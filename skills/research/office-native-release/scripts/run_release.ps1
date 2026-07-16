param(
    [Parameter(Mandatory = $true)]
    [string]$Spec,

    [Parameter(Mandatory = $true)]
    [string]$RenderDir,

    [string]$ExportLog,

    [switch]$SkipExport,

    [switch]$OverwritePdf
)

$ErrorActionPreference = 'Stop'

function Resolve-SpecPath {
    param(
        [string]$Base,
        [string]$Value
    )
    if ([System.IO.Path]::IsPathRooted($Value)) {
        return [System.IO.Path]::GetFullPath($Value)
    }
    return [System.IO.Path]::GetFullPath((Join-Path $Base $Value))
}

function Find-CodexPython {
    if ($env:CODEX_PYTHON -and (Test-Path -LiteralPath $env:CODEX_PYTHON)) {
        return (Resolve-Path -LiteralPath $env:CODEX_PYTHON).Path
    }
    $candidate = Join-Path $HOME '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $candidate) {
        return $candidate
    }
    $command = Get-Command python -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }
    throw 'Python runtime not found. Load Codex workspace dependencies or set CODEX_PYTHON.'
}

$specPath = (Resolve-Path -LiteralPath $Spec).Path
$specBase = Split-Path -Parent $specPath
$specData = Get-Content -LiteralPath $specPath -Raw -Encoding UTF8 | ConvertFrom-Json
$sourceValue = if ($specData.source) {
    $specData.source
}
elseif ($specData.docx) {
    $specData.docx
}
elseif ($specData.pptx) {
    $specData.pptx
}
else {
    throw 'Spec must define source, docx, or pptx.'
}

$sourcePath = Resolve-SpecPath -Base $specBase -Value $sourceValue
$pdfPath = Resolve-SpecPath -Base $specBase -Value $specData.pdf
$renderPath = Resolve-SpecPath -Base $specBase -Value $RenderDir
$python = Find-CodexPython
$scriptDirectory = $PSScriptRoot

if (-not $SkipExport) {
    $exportParameters = @{
        InputPath = $sourcePath
        OutputPdf = $pdfPath
    }
    if ($ExportLog) {
        $exportParameters.LogPath = Resolve-SpecPath -Base $specBase -Value $ExportLog
    }
    if ($OverwritePdf) {
        $exportParameters.Overwrite = $true
    }
    & (Join-Path $scriptDirectory 'export_office_pdf.ps1') @exportParameters
}
elseif (-not (Test-Path -LiteralPath $pdfPath)) {
    throw "SkipExport was requested but the PDF does not exist: $pdfPath"
}

& $python (Join-Path $scriptDirectory 'qa_release.py') --spec $specPath
if ($LASTEXITCODE -ne 0) {
    throw "Structural release QA failed with exit code $LASTEXITCODE"
}

& $python (Join-Path $scriptDirectory 'render_pdf.py') $pdfPath --output-dir $renderPath --dpi 180
if ($LASTEXITCODE -ne 0) {
    throw "PDF rendering failed with exit code $LASTEXITCODE"
}

[ordered]@{
    structural_and_render_checks_passed = $true
    office_source = $sourcePath
    pdf = $pdfPath
    spec = $specPath
    render_directory = $renderPath
    visual_inspection_pending = $true
} | ConvertTo-Json -Depth 5
