# MCP demo — let an LLM debug through Grafana (speaker only)

Verified with `grafana/mcp-grafana:2.0.2` against this stack on 2026-10-16.

## 1. A Viewer-only token

```bash
docker compose up -d            # stack must be running
./mcp/create-token.sh           # creates service account "mcp-viewer" (Viewer role) → mcp/.token
```

## 2. Connect your MCP client

**Claude Code** (run from the repo root):

```bash
claude mcp add grafana \
  -e GRAFANA_SERVICE_ACCOUNT_TOKEN="$(cat mcp/.token)" \
  -- docker run --rm -i --network the-3am-page_default \
     -e GRAFANA_URL=http://grafana:3000 -e GRAFANA_SERVICE_ACCOUNT_TOKEN \
     grafana/mcp-grafana:2.0.2 -t stdio --usage-stats=disabled --disable-write \
     --enabled-tools search,datasource,prometheus,alerting,dashboard
```

Check: `claude mcp list` → `grafana ✓ connected`.

Why each flag:

| Flag | Why |
|---|---|
| `-t stdio` | the image defaults to **SSE on 0.0.0.0:8000 with no auth** — never do that on venue wifi |
| `--network the-3am-page_default` | reach Grafana by its compose name |
| `--disable-write` | no create/update tools (the Viewer token blocks writes anyway — two layers) |
| `--enabled-tools …` | 19 tools instead of 100+: less context for the model, fewer ways to wander |
| `--usage-stats=disabled` | the server reports anonymous usage stats by default |

## 3. The 19 tools in this config

`search_dashboards` `search_folders` `get_dashboard_by_uid` `get_dashboard_summary` `get_dashboard_property`
`get_dashboard_panel_queries` `list_dashboard_versions` `list_datasources` `get_datasource`
`check_datasources_health` `query_prometheus` `query_prometheus_histogram` `list_prometheus_metric_names`
`list_prometheus_metric_metadata` `list_prometheus_label_names` `list_prometheus_label_values`
`alerting_rules_read` `alerting_silences_read` `alerting_manage_routing`

## 4. Run the demo

1. Turn chaos on **before** the MCP slide: `curl -X POST localhost:8080/chaos -d '{"latency_ms":1200}'`
2. Wait ~60s so the graphs show it.
3. Paste the prompt from [prompt.md](prompt.md).

What a good run does (verified tool calls, real values from the dry run):

```
search_dashboards(query="checkout")           → "Checkout — RED" (uid checkout-red)
query_prometheus(p99 by route, instant)       → /checkout 2.48s, /products 0.05s
query_prometheus(chaos_latency_seconds)       → 1.2
```

## 5. If it fails on stage

Play `speaker/mcp-demo.mp4` (record it on the dry run!) and narrate over it.
