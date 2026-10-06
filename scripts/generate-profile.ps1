param(
  [string]$Profile = (Join-Path $PSScriptRoot "..\examples\marie-curie\profile.json"),
  [string]$Output = (Join-Path $PSScriptRoot "..\generated-profile"),
  [switch]$Render
)
$ErrorActionPreference = "Stop"
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Python = Get-Command py -ErrorAction SilentlyContinue
if (-not $Python) { $Python = Get-Command python -ErrorAction SilentlyContinue }
if (-not $Python) { throw "Python 3 is required." }
$args = @((Join-Path $Root "scripts\profile_generator.py"), $Profile, "--output", $Output, "--validate")
if ($Render) { $args += "--render" }
& $Python.Source @args
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
