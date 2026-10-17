# The 3 AM Page

Code for the hands-on observability workshop I'm running at Cloud Native Mumbai × Grafana & Friends Mumbai on 17 Oct 2026.
We instrument a small service, scrape it with Prometheus, build a dashboard in Grafana, break the service on purpose and watch an alert fire.

— [Afzal Hassan](https://www.linkedin.com/in/iemafzalhassan/)

**Slides:** [`slides/the-3am-page.pdf`](slides/the-3am-page.pdf) · **Sources for every claim:** [REFERENCES.md](REFERENCES.md)

## Before the workshop (do this at home!)

```bash
git clone https://github.com/iemafzalhassan/the-3am-page
cd the-3am-page
./preflight.sh            # Windows (PowerShell): .\preflight.ps1
```

You need Docker Desktop (or Docker Engine) with Compose v2 or newer, ~3 GB of memory for Docker and ~1 GB of disk.
Preflight checks everything, downloads the images, and ends with **✅ Ready for 17 Oct**.

## Start

```bash
docker compose up -d
```

| What | Where |
|---|---|
| The app | http://localhost:8080/products |
| Prometheus | http://localhost:9090 |
| Grafana | http://localhost:3000 — `admin` / `admin` |
| alert-sink | http://localhost:5001 |

Grafana needs ~60 seconds on first start.

## Fell behind? Jump to a checkpoint

```bash
./checkpoint.sh 3        # Windows: .\checkpoint.ps1 3
```

| Checkpoint | You get |
|---|---|
| `1`, `2` | nothing to copy: just make sure the stack is up (PromQL exercises are in `exercises/`) |
| `3` | the finished **Checkout — RED** dashboard |
| `4` | the Grafana alert `CheckoutP99High` wired to alert-sink |
| `reset` | back to the bare starting point |

It only copies files from `checkpoints/` and restarts Grafana, so it works from the pen-drive zip too.

## Break it on purpose

```bash
curl -X POST localhost:8080/chaos -d '{"latency_ms": 1200}'   # slow checkouts
curl -X POST localhost:8080/chaos -d '{"error_rate": 0.3}'    # 30% failing checkouts
curl -X POST localhost:8080/chaos -d ''                       # back to normal
```

## What's inside

```
app/          checkout-api (FastAPI) — also runs as loadgen and alert-sink
prometheus/   scrape config, alerting rules, rule unit tests
grafana/      provisioning (the Prometheus datasource)
checkpoints/  finished files for steps 3 and 4 (used by checkpoint.sh)
exercises/    PromQL questions
kind/         open-lab bonus: the same stack on Kubernetes
mcp/          speaker demo: let an LLM debug through Grafana's MCP server
offline/      build/load the pen-drive image bundle
```

## No internet at the venue?

Ask a volunteer for a pen drive, then:

```bash
./offline/load-bundle.sh        # loads images-<your-arch>.tar
```

## Something broken?

Open an issue, or grab me (or a volunteer with a red sticky note) during the workshop.

## Clean up

```bash
docker compose down -v
```
