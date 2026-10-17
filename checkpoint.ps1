# Fell behind? Jump to the finished state of a module (Windows PowerShell).
#   .\checkpoint.ps1 3      finished "Checkout — RED" dashboard
#   .\checkpoint.ps1 4      + the Grafana alert that lands on alert-sink
#   .\checkpoint.ps1 reset  back to the bare starting point
param([string]$Step)
Set-Location $PSScriptRoot

switch ($Step) {
  { $_ -in "1", "2" } { Write-Host "Step $Step needs no extra files, just a running stack."; docker compose up -d }
  { $_ -in "3", "4" } {
    foreach ($s in 3..[int]$Step) { Copy-Item -Recurse -Force "checkpoints\step-$s\*" . }
    docker compose up -d
    docker compose restart grafana
    Write-Host "At step $Step. Give Grafana ~20 s, then open http://localhost:3000" -ForegroundColor Green
  }
  "reset" {
    Remove-Item -ErrorAction SilentlyContinue grafana\dashboards\checkout-red.json, grafana\provisioning\dashboards\workshop.yml,
      grafana\provisioning\alerting\contact-points.yml, grafana\provisioning\alerting\policies.yml, grafana\provisioning\alerting\rules.yml
    docker compose up -d --force-recreate grafana
    Write-Host "Back to the starting point." -ForegroundColor Green
  }
  default { Write-Host "usage: .\checkpoint.ps1 1|2|3|4|reset"; exit 1 }
}
