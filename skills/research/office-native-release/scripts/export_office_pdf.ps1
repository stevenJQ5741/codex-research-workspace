param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$OutputPdf,

    [string]$LogPath,

    [switch]$Overwrite
)

$ErrorActionPreference = 'Stop'
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

$extension = [System.IO.Path]::GetExtension($sourcePath).ToLowerInvariant()
$stagingPath = if ($Overwrite) {
    Join-Path $outputDirectory ('.office-export-' + [Guid]::NewGuid().ToString('N') + '.pdf')
} else {
    $outputPath
}

$application = $null
$document = $null
$kind = $null
$officeVersion = $null
$started = Get-Date

try {
    if ($extension -in @('.docx', '.docm', '.dotx', '.dotm')) {
        $kind = 'Word'
        $application = New-Object -ComObject Word.Application
        $officeVersion = $application.Version
        $application.Visible = $false
        $application.DisplayAlerts = 0
        $application.ScreenUpdating = $false

        # Keep the call to the four stable leading arguments. Supplying the full
        # optional COM signature caused a NullReferenceException on this Office build.
        $document = $application.Documents.Open($sourcePath, $false, $true, $false)
        $document.Repaginate()
        $document.ExportAsFixedFormat($stagingPath, 17)
    }
    elseif ($extension -in @('.pptx', '.pptm', '.ppsx', '.ppsm', '.potx', '.potm')) {
        $kind = 'PowerPoint'
        $application = New-Object -ComObject PowerPoint.Application
        $officeVersion = $application.Version
        $document = $application.Presentations.Open($sourcePath, -1, 0, 0)
        $document.SaveAs($stagingPath, 32)
    }
    else {
        throw "Unsupported Office input extension: $extension"
    }

    if (-not (Test-Path -LiteralPath $stagingPath)) {
        throw 'Office export returned without creating a PDF.'
    }
    $outputInfo = Get-Item -LiteralPath $stagingPath
    if ($outputInfo.Length -lt 1024) {
        throw "Office export created an unexpectedly small PDF: $($outputInfo.Length) bytes"
    }

    if ($Overwrite) {
        Move-Item -LiteralPath $stagingPath -Destination $outputPath -Force
        $outputInfo = Get-Item -LiteralPath $outputPath
    }

    $result = [ordered]@{
        success = $true
        exporter = $kind
        office_version = $officeVersion
        source = $sourcePath
        source_sha256 = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
        output = $outputPath
        output_sha256 = (Get-FileHash -LiteralPath $outputPath -Algorithm SHA256).Hash
        output_bytes = $outputInfo.Length
        started_at = $started.ToString('o')
        completed_at = (Get-Date).ToString('o')
    }
    $json = $result | ConvertTo-Json -Depth 5
    if ($LogPath) {
        $resolvedLog = [System.IO.Path]::GetFullPath($LogPath)
        [System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($resolvedLog)) | Out-Null
        [System.IO.File]::WriteAllText($resolvedLog, $json, [System.Text.UTF8Encoding]::new($false))
    }
    $json
}
catch {
    $failure = [ordered]@{
        success = $false
        exporter = $kind
        office_version = $officeVersion
        source = $sourcePath
        output = $outputPath
        staging_output = $stagingPath
        error_type = $_.Exception.GetType().FullName
        error_message = $_.Exception.Message
        position = $_.InvocationInfo.PositionMessage
        script_stack = $_.ScriptStackTrace
        started_at = $started.ToString('o')
        failed_at = (Get-Date).ToString('o')
    }
    $failureJson = $failure | ConvertTo-Json -Depth 5
    if ($LogPath) {
        $resolvedLog = [System.IO.Path]::GetFullPath($LogPath)
        [System.IO.Directory]::CreateDirectory([System.IO.Path]::GetDirectoryName($resolvedLog)) | Out-Null
        [System.IO.File]::WriteAllText($resolvedLog, $failureJson, [System.Text.UTF8Encoding]::new($false))
    }
    Write-Error $failureJson
}
finally {
    if ($document) {
        try { $document.Close(0) } catch { }
        try { [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($document) } catch { }
    }
    if ($application) {
        try { $application.Quit() } catch { }
        try { [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($application) } catch { }
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
