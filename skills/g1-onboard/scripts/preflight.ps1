param([string]$Config = "config/robot.toml")

$ErrorActionPreference = "Stop"
$result = [ordered]@{
    config_exists = Test-Path -LiteralPath $Config
    git_available = $null -ne (Get-Command git -ErrorAction SilentlyContinue)
    python_available = $null -ne (Get-Command python3 -ErrorAction SilentlyContinue)
    platform = [System.Environment]::OSVersion.Platform.ToString()
}
$result | ConvertTo-Json
if (-not $result.config_exists) { exit 1 }

