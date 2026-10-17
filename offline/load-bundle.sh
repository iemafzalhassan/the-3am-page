#!/usr/bin/env bash
# Load images from the pen drive — no internet needed.   ./offline/load-bundle.sh [path/to/tar]
# Windows (PowerShell):  docker load -i E:\images-amd64.tar     (Apple Silicon / ARM: images-arm64.tar)
set -euo pipefail
cd "$(dirname "$0")"
case "$(uname -m)" in
  x86_64|amd64) arch=amd64 ;;
  arm64|aarch64) arch=arm64 ;;
  *) echo "unknown CPU $(uname -m) — pick images-amd64.tar or images-arm64.tar by hand"; exit 1 ;;
esac
tar="${1:-images-$arch.tar}"
echo "Loading $tar … (about a minute)"
docker load -i "$tar"
echo "✅ Done. Now:  docker compose up -d"
