$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$python = Join-Path $projectRoot ".venv-win\Scripts\python.exe"
if (-not (Test-Path -LiteralPath $python)) {
    throw "No se encontró el entorno .venv-win."
}

Write-Host "Migo en vivo: micrófono del PC -> ElevenLabs -> altavoz del G1"
Write-Host "Habla normalmente. Pulsa Ctrl+C para finalizar."
& $python -m g1edu.cli --config config\robot.toml converse
