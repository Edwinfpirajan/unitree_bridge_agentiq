param([string]$Config = "config/robot.toml")

$interfaces = Get-NetAdapter -ErrorAction SilentlyContinue |
    Select-Object Name, Status, LinkSpeed, MacAddress
[ordered]@{
    timestamp_utc = [DateTime]::UtcNow.ToString("o")
    hostname = [System.Net.Dns]::GetHostName()
    config_exists = Test-Path -LiteralPath $Config
    cyclone_dds_uri_set = -not [string]::IsNullOrWhiteSpace($env:CYCLONEDDS_URI)
    interfaces = $interfaces
} | ConvertTo-Json -Depth 4
