# Chocolatey Uninstall Script for Empirica

$ErrorActionPreference = 'Stop'

$packageName = 'empirica'

Write-Host "Uninstalling Empirica..." -ForegroundColor Cyan

# Uninstall via pip
$pipArgs = @(
    'uninstall',
    '-y',
    'empirica'
)

$exitCode = Start-ChocolateyProcessAsAdmin `
    -Statements ($pipArgs -join ' ') `
    -ExeToRun 'python' `
    -ValidExitCodes @(0) `
    -WorkingDirectory $env:TEMP

if ($exitCode -eq 0) {
    Write-Host "✓ Empirica uninstalled successfully!" -ForegroundColor Green
} else {
    Write-Warning "Uninstall completed with exit code: $exitCode"
}
