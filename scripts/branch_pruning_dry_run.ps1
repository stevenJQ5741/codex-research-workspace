[CmdletBinding()]
param(
    [string]$Remote = "origin",
    [Parameter(Mandatory = $true)]
    [string]$PreviousDefault,
    [string]$SnapshotTag,
    [string[]]$InactiveBranch = @(),
    [string[]]$ActiveBranch = @(),
    [string[]]$MilestoneBranch = @(),
    [datetimeoffset]$AsOf = [datetimeoffset]::Now,
    [string]$OutputPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repoRoot = Split-Path -Parent $PSScriptRoot

function Invoke-Git {
    $gitArguments = @($args)
    $output = & git -C $repoRoot @gitArguments 2>&1
    if ($LASTEXITCODE -ne 0) {
        throw "git $($gitArguments -join ' ') failed:`n$($output -join "`n")"
    }
    return @($output)
}

function Test-Ancestor {
    param(
        [string]$Ancestor,
        [string]$Descendant
    )

    & git -C $repoRoot merge-base --is-ancestor $Ancestor $Descendant 2>$null
    return ($LASTEXITCODE -eq 0)
}

function Format-Boolean {
    param([bool]$Value)
    if ($Value) { return "yes" }
    return "no"
}

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    throw "git is required."
}
if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    throw "GitHub CLI (gh) is required to verify open pull requests."
}

Invoke-Git fetch $Remote --tags | Out-Null

$headLines = Invoke-Git ls-remote --symref $Remote HEAD
$headLine = $headLines | Where-Object { $_ -match "^ref:\s+refs/heads/(.+)\s+HEAD$" } |
    Select-Object -First 1
if (-not $headLine) {
    throw "Cannot resolve the default branch from $Remote/HEAD."
}
$currentDefault = [regex]::Match($headLine, "^ref:\s+refs/heads/(.+)\s+HEAD$").Groups[1].Value

$remoteUrl = [string](Invoke-Git remote get-url $Remote | Select-Object -First 1)
$repositoryOutput = & gh repo view $remoteUrl --json nameWithOwner --jq ".nameWithOwner"
$repository = if ($repositoryOutput) { $repositoryOutput.Trim() } else { $null }
if ($LASTEXITCODE -ne 0 -or -not $repository) {
    throw "Cannot resolve the GitHub repository."
}

$openPrJson = & gh pr list --repo $repository --state open --limit 200 `
    --json headRefName,number,title
if ($LASTEXITCODE -ne 0) {
    throw "Cannot query open pull requests."
}
$openPrItems = if ($openPrJson.Trim() -eq "[]") {
    @()
} else {
    @($openPrJson | ConvertFrom-Json)
}
$openPrByBranch = @{}
foreach ($item in $openPrItems) {
    $openPrByBranch[[string]$item.headRefName] = [int]$item.number
}

$snapshotAvailable = $false
if ($SnapshotTag) {
    & git -C $repoRoot rev-parse --verify --quiet "refs/tags/$SnapshotTag" *> $null
    $snapshotAvailable = ($LASTEXITCODE -eq 0)
    if (-not $snapshotAvailable) {
        throw "Snapshot tag not found locally after fetch: $SnapshotTag"
    }
}

$cutoff = $AsOf.AddMonths(-6)
$branchLines = Invoke-Git for-each-ref "refs/remotes/$Remote" `
    "--format=%(refname:short)|%(objectname)|%(committerdate:iso-strict)"

$rows = @()
foreach ($line in $branchLines) {
    $parts = $line -split "\|", 3
    if ($parts.Count -ne 3 -or $parts[0] -eq $Remote -or $parts[0] -eq "$Remote/HEAD") {
        continue
    }

    $remoteRef = $parts[0]
    $branch = $remoteRef.Substring($Remote.Length + 1)
    $tip = $parts[1]
    $tipTime = [datetimeoffset]::Parse($parts[2])
    $olderThanSixMonths = $tipTime -lt $cutoff
    $hasOpenPr = $openPrByBranch.ContainsKey($branch)
    $explicitlyInactive = $InactiveBranch -contains $branch
    $declaredActive = $ActiveBranch -contains $branch
    $isMilestone = $MilestoneBranch -contains $branch
    $isCurrentDefault = $branch -eq $currentDefault
    $isPreviousDefault = $branch -eq $PreviousDefault

    $uniqueCount = [int](Invoke-Git rev-list --count "$Remote/$currentDefault..$remoteRef" |
        Select-Object -First 1)
    $coveredByDefault = Test-Ancestor -Ancestor $tip -Descendant "$Remote/$currentDefault"
    $coveredBySnapshot = $false
    if ($snapshotAvailable) {
        $coveredBySnapshot = Test-Ancestor -Ancestor $tip -Descendant "refs/tags/$SnapshotTag"
    }
    $covered = $coveredByDefault -or $coveredBySnapshot
    $hasUnarchivedUniqueCommit = ($uniqueCount -gt 0) -and (-not $coveredBySnapshot)

    $protection = [System.Collections.Generic.List[string]]::new()
    if ($isCurrentDefault) { $protection.Add("current default") }
    if ($isPreviousDefault) { $protection.Add("previous default") }
    if ($hasOpenPr) { $protection.Add("open PR #$($openPrByBranch[$branch])") }
    if ($declaredActive) { $protection.Add("active work") }
    if ($isMilestone) { $protection.Add("user milestone") }
    if (-not $explicitlyInactive -and -not $declaredActive) {
        $protection.Add("activity not attested inactive")
    }
    if ($hasUnarchivedUniqueCommit) { $protection.Add("unarchived unique commit") }
    if (-not $covered) { $protection.Add("not covered") }

    $deleteCandidate =
        $olderThanSixMonths -and
        (-not $hasOpenPr) -and
        $explicitlyInactive -and
        (-not $declaredActive) -and
        (-not $isMilestone) -and
        (-not $isCurrentDefault) -and
        (-not $isPreviousDefault) -and
        (-not $hasUnarchivedUniqueCommit) -and
        $covered

    $rows += [pscustomobject]@{
        Branch = $branch
        Tip = $tip.Substring(0, 7)
        TipTime = $tipTime.ToString("yyyy-MM-dd HH:mm zzz")
        OlderThanSixMonths = Format-Boolean $olderThanSixMonths
        OpenPr = Format-Boolean $hasOpenPr
        UniqueCommits = $uniqueCount
        Covered = Format-Boolean $covered
        Protection = if ($protection.Count) { $protection -join "; " } else { "none" }
        DeleteCandidate = Format-Boolean $deleteCandidate
    }
}

$markdown = [System.Collections.Generic.List[string]]::new()
$markdown.Add("# Branch Pruning Dry Run")
$markdown.Add("")
$markdown.Add(('- generated: `{0}`' -f $AsOf.ToString("o")))
$markdown.Add(('- repository: `{0}`' -f $repository))
$markdown.Add(('- current default: `{0}`' -f $currentDefault))
$markdown.Add(('- previous default: `{0}`' -f $PreviousDefault))
$markdown.Add(('- cutoff: `{0}`' -f $cutoff.ToString("o")))
$snapshotLabel = if ($SnapshotTag) { $SnapshotTag } else { "none" }
$markdown.Add(('- snapshot: `{0}`' -f $snapshotLabel))
$markdown.Add('- remote deletion performed: `no`')
$markdown.Add("")
$markdown.Add("| Remote branch | Tip | Tip time | Older than 6 months | Open PR | Unique commits vs current default | Covered by default or snapshot | Protection | Delete candidate |")
$markdown.Add("| --- | --- | --- | --- | --- | ---: | --- | --- | --- |")
foreach ($row in $rows | Sort-Object Branch) {
    $markdown.Add(('| `{0}` | `{1}` | {2} | {3} | {4} | {5} | {6} | {7} | {8} |' -f
        $row.Branch,
        $row.Tip,
        $row.TipTime,
        $row.OlderThanSixMonths,
        $row.OpenPr,
        $row.UniqueCommits,
        $row.Covered,
        $row.Protection,
        $row.DeleteCandidate))
}
$markdown.Add("")
$markdown.Add('A `yes` result is only a candidate. Remote deletion still requires a separate explicit approval.')

$text = $markdown -join [Environment]::NewLine
if ($OutputPath) {
    $resolvedOutput = [System.IO.Path]::GetFullPath($OutputPath)
    $outputDirectory = Split-Path -Parent $resolvedOutput
    if ($outputDirectory) {
        New-Item -ItemType Directory -Path $outputDirectory -Force | Out-Null
    }
    Set-Content -LiteralPath $resolvedOutput -Value $text -Encoding UTF8
}

$text
