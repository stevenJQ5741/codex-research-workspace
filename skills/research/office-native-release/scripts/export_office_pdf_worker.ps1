param(
    [Parameter(Mandatory = $true)]
    [string]$InputPath,

    [Parameter(Mandatory = $true)]
    [string]$StagingPdf,

    [Parameter(Mandatory = $true)]
    [string]$ResultPath,

    [Parameter(Mandatory = $true)]
    [string]$ProcessMetadataPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;

public static class OfficeNativeWindowProcess {
    [DllImport("user32.dll")]
    public static extern uint GetWindowThreadProcessId(IntPtr hWnd, out uint processId);
}
'@

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
        ($Value | ConvertTo-Json -Depth 8),
        [System.Text.UTF8Encoding]::new($false)
    )
}

function Get-OfficeProcessId {
    param([Parameter(Mandatory = $true)][object]$Application)

    $windowHandle = [IntPtr]::Zero
    if ($Application.PSObject.Properties.Name -contains 'Hwnd') {
        $windowHandle = [IntPtr]$Application.Hwnd
    }
    elseif ($Application.PSObject.Properties.Name -contains 'HWND') {
        $windowHandle = [IntPtr]$Application.HWND
    }
    if ($windowHandle -eq [IntPtr]::Zero) {
        return $null
    }

    [uint32]$processId = 0
    [void][OfficeNativeWindowProcess]::GetWindowThreadProcessId(
        $windowHandle,
        [ref]$processId
    )
    if ($processId -eq 0) {
        return $null
    }
    return [int]$processId
}

$sourcePath = (Resolve-Path -LiteralPath $InputPath).Path
$stagingPath = [System.IO.Path]::GetFullPath($StagingPdf)
$resultFile = [System.IO.Path]::GetFullPath($ResultPath)
$processMetadataFile = [System.IO.Path]::GetFullPath($ProcessMetadataPath)
$extension = [System.IO.Path]::GetExtension($sourcePath).ToLowerInvariant()
$application = $null
$document = $null
$printRange = $null
$kind = $null
$officeVersion = $null
$officeProcessId = $null
$sourceUnits = $null
$started = Get-Date
$exitCode = 0

try {
    if ($extension -in @('.docx', '.docm', '.dotx', '.dotm')) {
        $kind = 'Word'
        $application = New-Object -ComObject Word.Application
        $officeVersion = $application.Version
        $application.Visible = $false
        $application.DisplayAlerts = 0
        $application.ScreenUpdating = $false
        $officeProcessId = Get-OfficeProcessId -Application $application
        Write-Utf8Json -Path $processMetadataFile -Value ([ordered]@{
            exporter = $kind
            office_pid = $officeProcessId
            worker_pid = $PID
            started_at = $started.ToString('o')
        })

        $document = $application.Documents.Open($sourcePath, $false, $true, $false)
        $document.Repaginate()
        $sourceUnits = $document.ComputeStatistics(2)
        $document.ExportAsFixedFormat($stagingPath, 17)
    }
    elseif ($extension -in @('.pptx', '.pptm', '.ppsx', '.ppsm', '.potx', '.potm')) {
        $kind = 'PowerPoint'
        [void][Reflection.Assembly]::LoadWithPartialName(
            'Microsoft.Office.Interop.PowerPoint'
        )
        [void][Reflection.Assembly]::LoadWithPartialName('Office')
        $application = New-Object -ComObject PowerPoint.Application
        $officeVersion = $application.Version
        $officeProcessId = Get-OfficeProcessId -Application $application
        Write-Utf8Json -Path $processMetadataFile -Value ([ordered]@{
            exporter = $kind
            office_pid = $officeProcessId
            worker_pid = $PID
            started_at = $started.ToString('o')
        })

        $document = $application.Presentations.Open($sourcePath, -1, 0, 0)
        $sourceUnits = $document.Slides.Count
        $document.PrintOptions.Ranges.ClearAll()
        $printRange = $document.PrintOptions.Ranges.Add(1, $sourceUnits)
        $document.ExportAsFixedFormat(
            $stagingPath,
            [Microsoft.Office.Interop.PowerPoint.PpFixedFormatType]::ppFixedFormatTypePDF,
            [Microsoft.Office.Interop.PowerPoint.PpFixedFormatIntent]::ppFixedFormatIntentPrint,
            [Microsoft.Office.Core.MsoTriState]::msoFalse,
            [Microsoft.Office.Interop.PowerPoint.PpPrintHandoutOrder]::ppPrintHandoutHorizontalFirst,
            [Microsoft.Office.Interop.PowerPoint.PpPrintOutputType]::ppPrintOutputSlides,
            [Microsoft.Office.Core.MsoTriState]::msoFalse,
            $printRange,
            [Microsoft.Office.Interop.PowerPoint.PpPrintRangeType]::ppPrintAll,
            '',
            $true,
            $true,
            $true,
            $true,
            $false
        )
    }
    else {
        throw "Unsupported Office input extension: $extension"
    }

    Write-Utf8Json -Path $resultFile -Value ([ordered]@{
        success = $true
        exporter = $kind
        export_method = 'ExportAsFixedFormat'
        office_version = $officeVersion
        office_pid = $officeProcessId
        worker_pid = $PID
        source = $sourcePath
        staging_output = $stagingPath
        source_units = $sourceUnits
        started_at = $started.ToString('o')
        completed_at = (Get-Date).ToString('o')
    })
}
catch {
    $exitCode = 1
    Write-Utf8Json -Path $resultFile -Value ([ordered]@{
        success = $false
        exporter = $kind
        export_method = 'ExportAsFixedFormat'
        office_version = $officeVersion
        office_pid = $officeProcessId
        worker_pid = $PID
        source = $sourcePath
        staging_output = $stagingPath
        error_type = $_.Exception.GetType().FullName
        error_message = $_.Exception.Message
        position = $_.InvocationInfo.PositionMessage
        script_stack = $_.ScriptStackTrace
        started_at = $started.ToString('o')
        failed_at = (Get-Date).ToString('o')
    })
}
finally {
    if ($printRange) {
        try {
            [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject(
                $printRange
            )
        }
        catch { }
    }
    if ($document) {
        try {
            if ($kind -eq 'PowerPoint') {
                $document.Close()
            }
            else {
                $document.Close(0)
            }
        }
        catch { }
        try {
            [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($document)
        }
        catch { }
    }
    if ($application) {
        try { $application.Quit() } catch { }
        try {
            [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($application)
        }
        catch { }
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}

exit $exitCode
