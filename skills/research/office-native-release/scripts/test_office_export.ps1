param(
    [Parameter(Mandatory = $true)]
    [string]$WorkRoot,

    [ValidateRange(10, 1800)]
    [int]$TimeoutSeconds = 90,

    [ValidateRange(180, 600)]
    [int]$Dpi = 180
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Find-CodexPython {
    if ($env:CODEX_PYTHON -and (Test-Path -LiteralPath $env:CODEX_PYTHON)) {
        return (Resolve-Path -LiteralPath $env:CODEX_PYTHON).Path
    }

    $userProfile = [System.Environment]::GetFolderPath(
        [System.Environment+SpecialFolder]::UserProfile
    )
    $candidate = Join-Path $userProfile `
        '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
    if (Test-Path -LiteralPath $candidate) {
        return $candidate
    }

    $command = Get-Command python -ErrorAction SilentlyContinue
    if ($command) {
        return $command.Source
    }
    throw 'Python runtime not found. Load Codex workspace dependencies or set CODEX_PYTHON.'
}

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
        ($Value | ConvertTo-Json -Depth 12),
        [System.Text.UTF8Encoding]::new($false)
    )
}

function Release-ComObject {
    param([object]$Value)
    if ($Value) {
        try {
            [void][System.Runtime.InteropServices.Marshal]::FinalReleaseComObject($Value)
        }
        catch { }
    }
}

function Convert-CodePointsToString {
    param([Parameter(Mandatory = $true)][int[]]$CodePoints)
    return -join @($CodePoints | ForEach-Object { [char]$_ })
}

function New-WordFixture {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Token,

        [Parameter(Mandatory = $true)]
        [string]$FormulaMarker,

        [Parameter(Mandatory = $true)]
        [string]$RandomCharacters,

        [Parameter(Mandatory = $true)]
        [string]$UnicodeFormula,

        [Parameter(Mandatory = $true)]
        [string]$WordEquation
    )

    $application = $null
    $document = $null
    $equationRange = $null
    try {
        $application = New-Object -ComObject Word.Application
        $application.Visible = $false
        $application.DisplayAlerts = 0
        $document = $application.Documents.Add()

        $document.Content.Text = @"
Native Office deterministic export test

Random token: $Token
Random characters: $RandomCharacters
$FormulaMarker
Unicode formula: $UnicodeFormula

Native Word equation:
"@

        $equationRange = $document.Range(
            $document.Content.End - 1,
            $document.Content.End - 1
        )
        $equationRange.Text = $WordEquation
        $equationRange.Font.Name = 'Cambria Math'
        [void]$document.OMaths.Add($equationRange)
        if ($document.OMaths.Count -gt 0) {
            $document.OMaths.Item($document.OMaths.Count).BuildUp()
        }

        $document.SaveAs2([System.IO.Path]::GetFullPath($Path), 16)
    }
    finally {
        if ($document) {
            try { $document.Close(0) } catch { }
        }
        if ($application) {
            try { $application.Quit() } catch { }
        }
        Release-ComObject -Value $equationRange
        Release-ComObject -Value $document
        Release-ComObject -Value $application
        [GC]::Collect()
        [GC]::WaitForPendingFinalizers()
    }
}

function New-PowerPointFixture {
    param(
        [Parameter(Mandatory = $true)]
        [string]$Path,

        [Parameter(Mandatory = $true)]
        [string]$Token,

        [Parameter(Mandatory = $true)]
        [string]$FormulaMarker,

        [Parameter(Mandatory = $true)]
        [string]$RandomCharacters,

        [Parameter(Mandatory = $true)]
        [string]$UnicodeFormula
    )

    $application = $null
    $presentation = $null
    $slide = $null
    $textBox = $null
    try {
        $application = New-Object -ComObject PowerPoint.Application
        $presentation = $application.Presentations.Add()
        $slide = $presentation.Slides.Add(1, 12)
        $textBox = $slide.Shapes.AddTextbox(1, 45, 40, 870, 440)
        $textBox.TextFrame.TextRange.Text = @"
Native Office deterministic export test

Random token: $Token
Random characters: $RandomCharacters
$FormulaMarker

$UnicodeFormula
"@
        $textBox.TextFrame.TextRange.Font.Name = 'Arial'
        $textBox.TextFrame.TextRange.Font.Size = 24
        $presentation.SaveAs([System.IO.Path]::GetFullPath($Path), 24)
    }
    finally {
        if ($presentation) {
            try { $presentation.Close() } catch { }
        }
        if ($application) {
            try { $application.Quit() } catch { }
        }
        Release-ComObject -Value $textBox
        Release-ComObject -Value $slide
        Release-ComObject -Value $presentation
        Release-ComObject -Value $application
        [GC]::Collect()
        [GC]::WaitForPendingFinalizers()
    }
}

function Get-PageImageRecords {
    param([Parameter(Mandatory = $true)][string]$RenderDirectory)

    $records = @(
        Get-ChildItem -LiteralPath $RenderDirectory -Filter 'page-*.png' -File |
            Sort-Object Name |
            ForEach-Object {
                [ordered]@{
                    name = $_.Name
                    bytes = $_.Length
                    sha256 = (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash
                }
            }
    )
    return ,$records
}

$workBase = [System.IO.Path]::GetFullPath($WorkRoot)
$runDirectory = Join-Path $workBase (
    'office-export-' +
    (Get-Date -Format 'yyyyMMdd-HHmmss') +
    '-' +
    [Guid]::NewGuid().ToString('N').Substring(0, 8)
)
[System.IO.Directory]::CreateDirectory($runDirectory) | Out-Null

$token = 'RND-' + [Guid]::NewGuid().ToString('N').Substring(0, 16).ToUpperInvariant()
$formulaMarker = 'FORMULA-MARKER-E-MC2'
$greek = Convert-CodePointsToString -CodePoints @(
    0x03B1, 0x20, 0x03B2, 0x20, 0x03B3, 0x20,
    0x0394, 0x20, 0x03A3, 0x20, 0x03A9
)
$chinese = Convert-CodePointsToString -CodePoints @(
    0x7814, 0x7A76, 0x9A8C, 0x8BC1
)
$japanese = Convert-CodePointsToString -CodePoints @(
    0x6570, 0x5F0F, 0x691C, 0x8A3C
)
$superscriptTwo = [char]0x00B2
$minusSign = [char]0x2212
$plusMinus = [char]0x00B1
$squareRoot = [char]0x221A
$integral = [char]0x222B
$subscriptZero = [char]0x2080
$superscriptOne = [char]0x00B9
$oneThird = [char]0x2153
$sigma = [char]0x03C3
$randomCharacters = "A7z9-Qx4P | $greek | $chinese | $japanese"
$unicodeFormula = (
    "E = mc$superscriptTwo; " +
    "x = ($minusSign" + "b $plusMinus $squareRoot" +
    "(b$superscriptTwo $minusSign 4ac))/(2a); " +
    "$integral$subscriptZero$superscriptOne x$superscriptTwo dx = $oneThird; " +
    "$sigma = F/A"
)
$wordEquation = (
    "x=(" + $minusSign + "b" + $plusMinus + $squareRoot +
    "(b^2" + $minusSign + "4ac))/(2a)"
)
$docxPath = Join-Path $runDirectory 'random-math.docx'
$pptxPath = Join-Path $runDirectory 'random-math.pptx'
$python = Find-CodexPython
$exportScript = Join-Path $PSScriptRoot 'export_office_pdf.ps1'
$qaScript = Join-Path $PSScriptRoot 'qa_release.py'
$renderScript = Join-Path $PSScriptRoot 'render_pdf.py'

New-WordFixture `
    -Path $docxPath `
    -Token $token `
    -FormulaMarker $formulaMarker `
    -RandomCharacters $randomCharacters `
    -UnicodeFormula $unicodeFormula `
    -WordEquation $wordEquation
New-PowerPointFixture `
    -Path $pptxPath `
    -Token $token `
    -FormulaMarker $formulaMarker `
    -RandomCharacters $randomCharacters `
    -UnicodeFormula $unicodeFormula

$fixtureResults = @()
foreach ($sourcePath in @($docxPath, $pptxPath)) {
    $kind = [System.IO.Path]::GetExtension($sourcePath).TrimStart('.').ToLowerInvariant()
    $exports = @()
    foreach ($number in 1..2) {
        $pdfPath = Join-Path $runDirectory "$kind-run$number.pdf"
        $exportLog = Join-Path $runDirectory "$kind-run$number-export.json"
        $renderDirectory = Join-Path $runDirectory "$kind-run$number-render"
        $qaReport = Join-Path $runDirectory "$kind-run$number-qa.json"
        $specPath = Join-Path $runDirectory "$kind-run$number-spec.json"

        $exportJson = & $exportScript `
            -InputPath $sourcePath `
            -OutputPdf $pdfPath `
            -LogPath $exportLog `
            -TimeoutSeconds $TimeoutSeconds
        $exportResult = $exportJson | ConvertFrom-Json
        if (-not $exportResult.success) {
            throw "Export run $number failed for $sourcePath"
        }

        $spec = [ordered]@{
            source = $sourcePath
            pdf = $pdfPath
            report = $qaReport
            expected_pages = [int]$exportResult.source_units
            required_strings = @($token, $formulaMarker)
            forbidden_strings = @('INTERNAL-ONLY-FAILURE-MARKER')
            minimum_text_characters_per_page = 10
        }
        if ($kind -eq 'pptx') {
            $spec.expected_slides = [int]$exportResult.source_units
        }
        Write-Utf8Json -Path $specPath -Value $spec

        & $python $qaScript --spec $specPath
        if ($LASTEXITCODE -ne 0) {
            throw "Pair QA run $number failed for $sourcePath with exit code $LASTEXITCODE"
        }

        & $python $renderScript $pdfPath --output-dir $renderDirectory --dpi $Dpi
        if ($LASTEXITCODE -ne 0) {
            throw "Render run $number failed for $sourcePath with exit code $LASTEXITCODE"
        }

        $exports += [ordered]@{
            run = $number
            pdf = $pdfPath
            export_log = $exportLog
            qa_report = $qaReport
            render_directory = $renderDirectory
            pages = Get-PageImageRecords -RenderDirectory $renderDirectory
        }
    }

    $firstPages = @($exports[0].pages)
    $secondPages = @($exports[1].pages)
    $deterministic = $firstPages.Count -eq $secondPages.Count
    if ($deterministic) {
        for ($index = 0; $index -lt $firstPages.Count; $index += 1) {
            if (
                $firstPages[$index].name -ne $secondPages[$index].name -or
                $firstPages[$index].sha256 -ne $secondPages[$index].sha256
            ) {
                $deterministic = $false
                break
            }
        }
    }
    if (-not $deterministic) {
        throw "Rendered pages are not deterministic across two native exports: $sourcePath"
    }

    $fixtureResults += [ordered]@{
        source = $sourcePath
        source_sha256 = (Get-FileHash -LiteralPath $sourcePath -Algorithm SHA256).Hash
        deterministic_page_renders = $deterministic
        exports = $exports
    }
}

$summary = [ordered]@{
    success = $true
    release_status = 'VISUAL_REVIEW_REQUIRED'
    run_directory = $runDirectory
    random_token = $token
    formula_marker = $formulaMarker
    export_runs_per_fixture = 2
    dpi = $Dpi
    fixtures = $fixtureResults
    full_size_visual_inspection_required = $true
}
$summaryPath = Join-Path $runDirectory 'smoke_summary.json'
Write-Utf8Json -Path $summaryPath -Value $summary
$summary | ConvertTo-Json -Depth 12
