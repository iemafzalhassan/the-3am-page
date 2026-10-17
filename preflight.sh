#!/usr/bin/env bash
# Preflight for "The 3 AM Page" workshop. Run at home, before 17 Oct:  ./preflight.sh
# Works with the bash that ships on macOS (3.2) and on Linux.
set -u
cd "$(dirname "$0")"

GREEN=$'\033[32m'; RED=$'\033[31m'; YELLOW=$'\033[33m'; DIM=$'\033[2m'; OFF=$'\033[0m'
FAILED=0
ok()   { printf "  ${GREEN}✔${OFF} %s\n" "$1"; }
bad()  { printf "  ${RED}✖${OFF} %s\n      ${DIM}→ %s${OFF}\n" "$1" "$2"; FAILED=1; }
warn() { printf "  ${YELLOW}!${OFF} %s\n      ${DIM}→ %s${OFF}\n" "$1" "$2"; }

echo "The 3 AM Page · preflight"
echo

# 1. Docker CLI and daemon
if ! command -v docker >/dev/null 2>&1; then
  bad "docker not found" "install Docker Desktop (macOS/Windows) or Docker Engine (Linux)"
  echo; echo "${RED}Fix the items above and run ./preflight.sh again.${OFF}"; exit 1
fi
if ! docker info >/dev/null 2>&1; then
  bad "Docker is installed but not running" "start Docker Desktop, or: sudo systemctl start docker (Linux: is your user in the docker group?)"
  echo; echo "${RED}Fix the items above and run ./preflight.sh again.${OFF}"; exit 1
fi
ok "Docker $(docker version --format '{{.Server.Version}}' 2>/dev/null)"

# 2. Compose v2 (the 'docker compose' plugin, not the old 'docker-compose')
if docker compose version >/dev/null 2>&1; then
  ok "Compose $(docker compose version --short 2>/dev/null)"
else
  bad "Docker Compose v2 not found" "update Docker Desktop, or install the docker-compose-plugin package"
fi

# 3. Memory available to Docker (on Mac/Windows this is the Docker Desktop VM)
mem=$(docker info --format '{{.MemTotal}}' 2>/dev/null || echo 0)
mem_gb=$(awk "BEGIN { printf \"%.1f\", $mem / 1073741824 }")
if awk "BEGIN { exit !($mem >= 3000000000) }"; then
  ok "${mem_gb} GB memory for Docker"
elif awk "BEGIN { exit !($mem >= 2000000000) }"; then
  warn "only ${mem_gb} GB memory for Docker" "it will probably work; close Chrome tabs on the day, or raise it in Docker Desktop → Settings → Resources"
else
  bad "only ${mem_gb} GB memory for Docker" "give Docker at least 3 GB: Docker Desktop → Settings → Resources"
fi

# 4. Ports (a port used by THIS workshop's own containers is fine)
service_for() { case "$1" in 8080) echo checkout-api;; 5001) echo alert-sink;; 9090) echo prometheus;; 3000) echo grafana;; esac; }
busy=""
for port in 8080 9090 3000 5001; do
  if (exec 3<>"/dev/tcp/127.0.0.1/$port") 2>/dev/null; then
    if docker compose port "$(service_for $port)" "$port" >/dev/null 2>&1; then
      continue  # it's our own stack, already running
    fi
    busy="$busy $port"
  fi
done
if [ -z "$busy" ]; then
  ok "ports 8080 9090 3000 5001 free"
else
  for port in $busy; do
    bad "port $port is busy" "something else is listening on $port — stop it (another Grafana, a dev server?)  see who: lsof -i :$port"
  done
fi

# 5. Images (download now, at home — not on venue wifi)
echo "  … pulling images (one-time, ~700 MB)"
if docker compose pull --quiet --ignore-buildable >/dev/null 2>&1 && docker compose build --quiet >/dev/null 2>&1; then
  size=$(docker image inspect prom/prometheus:v3.15.0 grafana/grafana:13.2.4 ghcr.io/iemafzalhassan/checkout-api:1.0 \
          --format '{{.Size}}' 2>/dev/null | awk '{ s += $1 } END { printf "%d", s / 1048576 }')
  ok "images ready (${size} MB)"
else
  bad "could not download or build the images" "check your internet connection and run ./preflight.sh again (or ask for a pen drive on the day)"
fi

echo
if [ "$FAILED" = 0 ]; then
  echo "${GREEN}✅ Ready for 17 Oct.${OFF} See you there!"
else
  echo "${RED}Fix the items marked ✖ and run ./preflight.sh again.${OFF}"
  exit 1
fi
