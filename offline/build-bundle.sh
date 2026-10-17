#!/usr/bin/env bash
# Build the pen-drive bundle: one image tarball per CPU architecture.
#   ./offline/build-bundle.sh            # amd64 and arm64
#   ./offline/build-bundle.sh amd64      # just one
# arm64 on an x86 machine needs QEMU:  docker run --privileged --rm tonistiigi/binfmt --install arm64
set -euo pipefail
cd "$(dirname "$0")/.."

APP=ghcr.io/iemafzalhassan/checkout-api:1.0
UPSTREAM="prom/prometheus:v3.15.0 grafana/grafana:13.2.4"
SAVE_PLATFORM=""
docker save --help 2>/dev/null | grep -q -- "--platform" && SAVE_PLATFORM=1

for arch in ${@:-amd64 arm64}; do
  echo "== linux/$arch"
  for img in $UPSTREAM; do docker pull --quiet --platform "linux/$arch" "$img"; done
  docker buildx build --quiet --platform "linux/$arch" -t "$APP" --load app
  out="offline/images-$arch.tar"
  if [ -n "$SAVE_PLATFORM" ]; then
    docker save --platform "linux/$arch" -o "$out" $UPSTREAM "$APP"
  else
    docker save -o "$out" $UPSTREAM "$APP"
  fi
  echo "   wrote $out ($(du -h "$out" | cut -f1))"
done

# leave this machine with images for its own architecture
native=$(docker version --format '{{.Server.Arch}}')
for img in $UPSTREAM; do docker pull --quiet --platform "linux/$native" "$img" >/dev/null; done
docker compose build --quiet
echo "Copy offline/images-*.tar, offline/load-bundle.sh and a zip of this repo to each pen drive."
