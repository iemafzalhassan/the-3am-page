# Preflight for "The 3 AM Page" workshop (Windows PowerShell 5.1+ / PowerShell 7).
# Run at home, before 17 Oct:   .\preflight.ps1
# If scripts are blocked:        powershell -ExecutionPolicy Bypass -File .\preflight.ps1
$ErrorActionPreference = "Continue"
Set-Location $PSScriptRoot
$failed = $false

function Ok($msg)            { Write-Host "  [OK] $msg" -ForegroundColor Green }
function Bad($msg, $hint)    { Write-Host "  [X]  $msg" -ForegroundColor Red; Write-Host "       -> $hint" -ForegroundColor DarkGray; $script:failed = $true }
function Warn($msg, $hint)   { Write-Host "  [!]  $msg" -ForegroundColor Yellow; Write-Host "       -> $hint" -ForegroundColor DarkGray }

Write-Host "The 3 AM Page - preflight`n"

# 1. Docker CLI and daemon
if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
    Bad "docker not found" "install Docker Desktop: https://docs.docker.com/desktop/setup/install/windows-install/"
    exit 1
}
docker info *> $null
if ($LASTEXITCODE -ne 0) {
    Bad "Docker is installed but not running" "start Docker Desktop and wait for 'Engine running' (WSL 2 backend recommended)"
    exit 1
}
Ok ("Docker " + (docker version --format '{{.Server.Version}}'))

# 2. Compose v2
docker compose version *> $null
if ($LASTEXITCODE -eq 0) { Ok ("Compose " + (docker compose version --short)) }
else { Bad "Docker Compose v2 not found" "update Docker Desktop" }

# 3. Memory available to Docker
$mem = [double](docker info --format '{{.MemTotal}}')
$gb = [math]::Round($mem / 1GB, 1)
if ($mem -ge 3e9)     { Ok "$gb GB memory for Docker" }
elseif ($mem -ge 2e9) { Warn "only $gb GB memory for Docker" "it will probably work; raise it in .wslconfig or Docker Desktop -> Settings -> Resources" }
else                  { Bad "only $gb GB memory for Docker" "give Docker at least 3 GB (.wslconfig: memory=4GB)" }

# 4. Ports (a port used by this workshop's own containers is fine)
$services = @{ 8080 = "checkout-api"; 9090 = "prometheus"; 3000 = "grafana"; 5001 = "alert-sink" }
$busy = @()
foreach ($port in 8080, 9090, 3000, 5001) {
    $client = New-Object System.Net.Sockets.TcpClient
    try {
        $client.Connect("127.0.0.1", $port)
        docker compose port $services[$port] $port *> $null
        if ($LASTEXITCODE -ne 0) { $busy += $port }
    } catch { } finally { $client.Close() }
}
if ($busy.Count -eq 0) { Ok "ports 8080 9090 3000 5001 free" }
else { foreach ($p in $busy) { Bad "port $p is busy" "find it with: Get-NetTCPConnection -LocalPort $p | Select OwningProcess" } }

# 5. Images
Write-Host "  ... pulling images (one-time, ~700 MB)"
docker compose pull --quiet --ignore-buildable *> $null
$pulled = $LASTEXITCODE
docker compose build --quiet *> $null
if ($pulled -eq 0 -and $LASTEXITCODE -eq 0) { Ok "images ready" }
else { Bad "could not download or build the images" "check your internet connection and run .\preflight.ps1 again" }

Write-Host ""
if (-not $failed) { Write-Host "Ready for 17 Oct. See you there!" -ForegroundColor Green }
else { Write-Host "Fix the items marked [X] and run .\preflight.ps1 again." -ForegroundColor Red; exit 1 }
