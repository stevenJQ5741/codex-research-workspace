[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [string]$DestinationRoot
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceRoot = Join-Path $repoRoot "skills"

if (-not $DestinationRoot) {
    $codexHome = if ($env:CODEX_HOME) {
        $env:CODEX_HOME
    } else {
        Join-Path $HOME ".codex"
    }
    $DestinationRoot = Join-Path $codexHome "skills"
}

if (-not (Test-Path -LiteralPath $sourceRoot -PathType Container)) {
    throw "Skills source directory not found: $sourceRoot"
}

New-Item -ItemType Directory -Path $DestinationRoot -Force | Out-Null

$skillFiles = Get-ChildItem -LiteralPath $sourceRoot -Recurse -Filter "SKILL.md" -File |
    Sort-Object FullName

if (-not $skillFiles) {
    throw "No SKILL.md files found under $sourceRoot"
}

$seenNames = @{}
$installed = 0

foreach ($skillFile in $skillFiles) {
    $content = Get-Content -LiteralPath $skillFile.FullName -Raw -Encoding UTF8
    if ($content -notmatch "(?m)^name:\s*([a-z0-9-]+)\s*$") {
        throw "Cannot read a valid Skill name from $($skillFile.FullName)"
    }

    $skillName = $Matches[1]
    if ($seenNames.ContainsKey($skillName)) {
        throw "Duplicate Skill name: $skillName"
    }
    $seenNames[$skillName] = $true

    $sourceDirectory = $skillFile.Directory.FullName
    $targetDirectory = Join-Path $DestinationRoot $skillName
    $marker = Join-Path $targetDirectory ".codex-research-workspace-managed"

    if (Test-Path -LiteralPath $targetDirectory) {
        if (-not (Test-Path -LiteralPath $marker -PathType Leaf)) {
            throw "Refusing to replace unmanaged Skill: $targetDirectory"
        }
        if ($PSCmdlet.ShouldProcess($targetDirectory, "Replace managed Skill")) {
            Remove-Item -LiteralPath $targetDirectory -Recurse -Force
        }
    }

    if ($PSCmdlet.ShouldProcess($targetDirectory, "Install Skill $skillName")) {
        Copy-Item -LiteralPath $sourceDirectory -Destination $targetDirectory -Recurse -Force
        Set-Content -LiteralPath $marker -Encoding ASCII -Value "source=codex-research-workspace"
        $installed += 1
    }
}

Write-Output "Installed $installed managed Skills to $DestinationRoot"
Write-Output "Restart Codex to refresh the available Skill catalog."
