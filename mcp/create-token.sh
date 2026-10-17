#!/usr/bin/env bash
# Creates a Viewer-only Grafana service account + token for the MCP demo.
#   ./mcp/create-token.sh        → prints the token and saves it to mcp/.token (git-ignored)
set -euo pipefail
cd "$(dirname "$0")"
G=${GRAFANA_URL:-http://localhost:3000}
AUTH=${GRAFANA_ADMIN:-admin:admin}

# Grafana takes ~60s on a fresh start; wait instead of failing with an empty reply.
for _ in $(seq 1 30); do
  curl -sf "$G/api/health" >/dev/null 2>&1 && break
  sleep 3
done
curl -sf -u "$AUTH" "$G/api/org" >/dev/null || { echo "Grafana at $G is not reachable with $AUTH — is the stack up?"; exit 1; }

sa_id=$(curl -sf -u "$AUTH" "$G/api/serviceaccounts/search?query=mcp-viewer" |
        python3 -c "import sys,json; a=json.load(sys.stdin)['serviceAccounts']; print(a[0]['id'] if a else '')")
if [ -z "$sa_id" ]; then
  sa_id=$(curl -sf -u "$AUTH" -H 'content-type: application/json' "$G/api/serviceaccounts" \
          -d '{"name":"mcp-viewer","role":"Viewer"}' | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
fi
token=$(curl -sf -u "$AUTH" -H 'content-type: application/json' "$G/api/serviceaccounts/$sa_id/tokens" \
        -d "{\"name\":\"mcp-$(date +%s)\"}" | python3 -c "import sys,json; print(json.load(sys.stdin)['key'])")
umask 077; printf '%s' "$token" > .token
echo "Viewer token saved to mcp/.token"
