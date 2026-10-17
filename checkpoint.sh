#!/usr/bin/env bash
# Fell behind? Jump to the finished state of a module.
#   ./checkpoint.sh 3       finished "Checkout — RED" dashboard
#   ./checkpoint.sh 4       + the Grafana alert that lands on alert-sink
#   ./checkpoint.sh reset   back to the bare starting point
# Works from a git clone or from the pen-drive zip (no git needed).
set -euo pipefail
cd "$(dirname "$0")"

case "${1:-}" in
  1|2)
    echo "Step $1 needs no extra files, just a running stack."
    docker compose up -d
    ;;
  3|4)
    for step in $(seq 3 "$1"); do cp -R "checkpoints/step-$step/." .; done
    docker compose up -d
    docker compose restart grafana   # Grafana reads provisioning files on start
    echo "✅ At step $1. Give Grafana ~20 s, then open http://localhost:3000"
    ;;
  reset)
    rm -f grafana/dashboards/checkout-red.json grafana/provisioning/dashboards/workshop.yml \
          grafana/provisioning/alerting/contact-points.yml grafana/provisioning/alerting/policies.yml \
          grafana/provisioning/alerting/rules.yml
    docker compose up -d --force-recreate grafana   # fresh Grafana, nothing provisioned
    echo "✅ Back to the starting point."
    ;;
  *)
    echo "usage: ./checkpoint.sh 1|2|3|4|reset"; exit 1 ;;
esac
