param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPdf,

    [string]$LogPath,

    [ValidateRange(10, 1800)]
    [int]$TimeoutSeconds = 90,

    [switch]$Overwrite
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Utf8Json {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [object]$Value
    )

    $resolvedPath = [System.IO.Path]::GetFullPath($Path)
    [System.IO.Directory]::CreateDirectory(
        [System.IO.Path]::GetDirectoryName($resolvedPath)
    ) | Out-Null
    [System.IO.File]::WriteAllText(
        $resolvedPath,
        ($Value | ConvertTo-Json -Depth 10),
        [System.Text.UTF8Encoding]::new($false)
    )
}

function Test-PdfHeader {
    param([Parameter(Mandatory = $true)][string]$Path)

    $stream = [System.IO.File]::Open(
        $Path,
        [System.IO.FileMode]::Open,
        [System.IO.FileAccess]::Read,
        [System.IO.FileShare]::ReadWrite
    )
    try {
        $buffer = [byte[]]::new(5)
        if ($stream.Read($buffer, 0, $buffer.Length) -ne $buffer.Length) {
            return $false
        }
        return [System.Text.Encoding]::ASCII.GetString($buffer) -eq '%PDF-'
    }
    finally {
        $stream.Dispose()
    }
}

function Wait-StableFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [int]$Attempts = 10,

        [int]$IntervalMilliseconds = 250
    )

    $previousLength = -1L
    $stableReads = 0
    for ($attempt = 0; $attempt -lt $Attempts; $attempt += 1) {
        if (Test-Path -LiteralPath $Path -PathType Leaf) {
            $length = (Get-Item -LiteralPath $Path).Length
            if ($length -gt 0 -and $length -eq $previousLength) {
                $stableReads += 1
                if ($stableReads -ge 2) {
                    return $length
                }
            }
            else {
                $stableReads = 0
            }
            $previousLength = $length
        }
        Start-Sleep -Milliseconds $IntervalMilliseconds
    }
    throw "Office export did not produce a stable file: $Path"
}

function Quote-ProcessArgument {
    param([Parameter(Mandatory = $true)][string]$Value)
    return '"' + $Value.Replace('"', '\"') + '"'
}

$sourcePath = (Resolve-Path -LiteralPath $InputPath).Path
$outputPath = [System.IO.Path]::GetFullPath($OutputPdf)
$outputDirectory = [System.IO.Path]::GetDirectoryName($outputPath)
[System.IO.Directory]::CreateDirectory($outputDirectory) | Out-Null

if ([System.IO.Path]::GetExtension($outputPath).ToLowerInvariant() -ne '.pdf') {
    throw 'OutputPdf must end in .pdf'
}
if ((Test-Path -LiteralPath $outputPath) -and -not $Overwrite) {
    throw "Output already exists. Pass -Overwrite to replace it: $outputPath"
}

$runId = [Guid]::NewGuid().ToString('N')
$stagingPath = Join-Path $outputDirectory ('.office-export-' + $runId + '.pdf')
$workerResultPath = Join-Path $outputDirectory ('.office-export-' + $runId + '.worker.json')
$processMetadataPath = Join-Path $outputDirectory ('.office-export-' + $runId + '.process.json')
$workerScript = Join-Path $PSScriptRoot 'export_office_pdf_worker.ps1'
$started = Get-Date
$process = $null
$completed = $false
$workerResult = $null

try {
    $powerShellExecutable = (Get-Command powershell.exe -ErrorAction Stop).Source
    $arguments = @(
        '-NoProfile',
        '-NonInteractive',
        '-ExecutionPolicy',
        'Bypass',
        '-File',
        (Quote-ProcessArgument -Value $workerScript),
        '-InputPath',
        (Quote-ProcessArgument -Value $sourcePath),
        '-StagingPdf',
        (Quote-ProcessArgument -Value $stagingPath),
        '-ResultPath',
        (Quote-ProcessArgument -Value $workerResultPath),
        '-ProcessMetadataPath',
        (Quote-ProcessArgument -Value $processMetadataPath)
    ) -join ' '

    $process = Start-Process `
        -FilePath $powerShellExecutable `
        -ArgumentList $arguments `
        -WindowStyle Hidden `
        -PassThru

    if (-not $process.WaitForExit($TimeoutSeconds * 1000)) {
        if (-not $process.HasExited) {
            Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        }
        if (Test-Path -LiteralPath $processMetadataPath -PathType Leaf) {
            $metadata = Get-Content -LiteralPath $processMetadataPath -Raw -Encoding UTF8 |
                ConvertFrom-Json
            if ($metadata.office_pid) {
                Stop-Process -Id ([int]$metadata.office_pid) -Force -ErrorAction SilentlyContinue
            }
        }
        throw "Native Office export timed out after $TimeoutSeconds second(s)."
    }

    if (-not (Test-Path -LiteralPath $workerResultPath -PathType Leaf)) {
        throw "Office export worker exited with code $($process.ExitCode) without a result file."
    }
    $workerResult = Get-Content -LiteralPath $workerResultPath -Raw -Encoding UTF8 |
        ConvertFrom-Json
    if ($process.ExitCode -ne 0 -or -not $workerResult.success) {
        $workerMessage = if ($workerResult.error_message) {
            $workerResult.error_message
        }
        else {
            "Worker exit code $($process.ExitCode)"
        }
        throw "Native Office export failed: $workerMessage"
    }

    $outputBytes = Wait-StableFile -Path $stagingPath
    if ($outputBytes -lt 1024) {
        throw "Office export created an unexpectedly small PDF: $outputBytes bytes"
    }
    if (-not (Test-PdfHeader -Path $stagingPath)) {
        throw 'Office export output does not start with a valid PDF header.'
    }

    if ((Test-Path -LiteralPath $outputPath) -and -not $Overwrite) {
        throw "Output appeared during export; refusing to overwrite it: $outputPath"
    }
    Move-Item -LiteralPath $stagingPath -Destination $outputPath -Force
    $outputInfo = Get-Item -LiteralPath $outputPath
    $result = [ordered]@{
        success = $true
        release_status = 'EXPORTED'
        exporter = $workerResult.exporter
        export_method = $workerResult.export_method
        office_version = $workerResult.office_version
        office_pid = $workerResult.office_pid
        worker_pid = $workerResult.worker_pid
        timeout_seconds = $TimeoutSeconds
        source = $sourcePath
        source_sha256 = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
        source_units = $workerResult.source_units
        output = $outputPath
        output_sha256 = (Get-FileHash -LiteralPath $outputPath -Algorithm SHA256).Hash
        output_bytes = $outputInfo.Length
        started_at = $started.ToString('o')
        completed_at = (Get-Date).ToString('o')
    }
    if ($LogPath) {
        Write-Utf8Json -Path $LogPath -Value $result
    }
    $completed = $true
    $result | ConvertTo-Json -Depth 10
}
catch {
    $failure = [ordered]@{
        success = $false
        release_status = 'FAILED'
        source = $sourcePath
        output = $outputPath
        staging_output = $stagingPath
        worker_result = $workerResult
        worker_result_path = $workerResultPath
        process_metadata_path = $processMetadataPath
        timeout_seconds = $TimeoutSeconds
        error_type = $_.Exception.GetType().FullName
        error_message = $_.Exception.Message
        position = $_.InvocationInfo.PositionMessage
        script_stack = $_.ScriptStackTrace
        started_at = $started.ToString('o')
        failed_at = (Get-Date).ToString('o')
    }
    if ($LogPath) {
        Write-Utf8Json -Path $LogPath -Value $failure
    }
    throw ($failure | ConvertTo-Json -Depth 10)
}
finally {
    if ($completed) {
        foreach ($path in @($workerResultPath, $processMetadataPath)) {
            if (Test-Path -LiteralPath $path -PathType Leaf) {
                Remove-Item -LiteralPath $path -Force
            }
        }
    }
}
