param(
    [string]$OutputJson
)

$ErrorActionPreference = 'Stop'

function Get-AppInfo {
    param([string]$Executable)

    $registryPath = "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\$Executable"
    $path = $null
    if (Test-Path -LiteralPath $registryPath) {
        $path = (Get-ItemProperty -LiteralPath $registryPath).'(default)'
    }
    if (-not $path) {
        $command = Get-Command $Executable -ErrorAction SilentlyContinue
        if ($command) {
            $path = $command.Source
        }
    }

    $version = $null
    if ($path -and (Test-Path -LiteralPath $path)) {
        $version = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($path).FileVersion
    }

    [ordered]@{
        installed = [bool]($path -and (Test-Path -LiteralPath $path))
        path = $path
        version = $version
    }
}

function Get-ComInfo {
    param([string]$ProgId)

    $registryPath = "Registry::HKEY_CLASSES_ROOT\$ProgId\CLSID"
    $clsid = $null
    if (Test-Path -LiteralPath $registryPath) {
        $clsid = (Get-Item -LiteralPath $registryPath).GetValue('')
    }
    [ordered]@{
        registered = [bool]$clsid
        clsid = $clsid
    }
}

function Get-PopplerInfo {
    $userProfile = [System.Environment]::GetFolderPath(
        [System.Environment+SpecialFolder]::UserProfile
    )
    $candidate = Join-Path $userProfile '.cache\codex-runtimes\codex-primary-runtime\dependencies\native\poppler\Library\bin\pdftoppm.exe'
    if (Test-Path -LiteralPath $candidate) {
        $path = $candidate
    }
    else {
        $command = Get-Command pdftoppm -ErrorAction SilentlyContinue
        $path = if ($command) { $command.Source } else { $null }
    }
    $version = $null
    if ($path -and $path.EndsWith('.exe') -and (Test-Path -LiteralPath $path)) {
        $version = [System.Diagnostics.FileVersionInfo]::GetVersionInfo($path).FileVersion
    }
    [ordered]@{
        available = [bool]$path
        path = $path
        version = $version
    }
}

$defaultPrinter = $null
$windowsProfilePath = 'HKCU:\Software\Microsoft\Windows NT\CurrentVersion\Windows'
if (Test-Path -LiteralPath $windowsProfilePath) {
    $defaultPrinter = (Get-ItemProperty -LiteralPath $windowsProfilePath -ErrorAction SilentlyContinue).Device
}

$profile = [ordered]@{
    generated_at_utc = [DateTime]::UtcNow.ToString('o')
    platform = [ordered]@{
        os = [System.Environment]::OSVersion.VersionString
        powershell = $PSVersionTable.PSVersion.ToString()
        architecture = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString()
    }
    word = Get-AppInfo -Executable 'WINWORD.EXE'
    powerpoint = Get-AppInfo -Executable 'POWERPNT.EXE'
    libreoffice = Get-AppInfo -Executable 'soffice.exe'
    com = [ordered]@{
        registration_check_only = $true
        word = Get-ComInfo -ProgId 'Word.Application'
        powerpoint = Get-ComInfo -ProgId 'PowerPoint.Application'
    }
    default_printer = $defaultPrinter
    poppler = Get-PopplerInfo
    release_policy = [ordered]@{
        authoritative_exporter = 'Microsoft Office COM'
        export_method = 'ExportAsFixedFormat'
        pdf_rasterizer = 'Poppler pdftoppm'
        libreoffice_primary_release_renderer = $false
        structural_layer_required = $true
        visual_layer_required = $true
        deterministic_smoke_test_required_after_environment_change = $true
    }
}

$json = $profile | ConvertTo-Json -Depth 8
if ($OutputJson) {
    $outputPath = [System.IO.Path]::GetFullPath($OutputJson)
    $outputDirectory = [System.IO.Path]::GetDirectoryName($outputPath)
    [System.IO.Directory]::CreateDirectory($outputDirectory) | Out-Null
    [System.IO.File]::WriteAllText($outputPath, $json, [System.Text.UTF8Encoding]::new($false))
}
$json
