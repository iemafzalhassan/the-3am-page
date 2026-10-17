# References

Every claim in the slides links to an official source. Slide numbers follow the deck in `slides/`.

**Slide 3**  
- [Docker Compose v5.5.1 release](https://github.com/docker/compose/releases/tag/v5.5.1)

**Slide 7**  
- [OpenTelemetry: Observability primer](https://opentelemetry.io/docs/concepts/observability-primer/)
- [Grafana Labs: What is observability?](https://grafana.com/blog/2022/07/01/what-is-observability-best-practices-key-metrics-methodologies-and-more)

**Slide 8**  
- [OpenTelemetry: What is OpenTelemetry?](https://opentelemetry.io/docs/what-is-opentelemetry/)
- [Prometheus docs: OTLP receiver](https://prometheus.io/docs/guides/opentelemetry/#enable-the-otlp-receiver)
- [Grafana docs: Data sources (Loki, Tempo)](https://grafana.com/docs/grafana/latest/datasources/)

**Slide 10**  
- [Prometheus docs: Overview (pull over HTTP)](https://prometheus.io/docs/introduction/overview/)
- [Grafana docs: Alerting fundamentals](https://grafana.com/docs/grafana/latest/alerting/fundamentals/)

**Slide 11**  
- [Docker docs: Networking in Compose](https://docs.docker.com/compose/how-tos/networking/)

**Slide 12**  
- [Docker docs: Compose ports (host IP binding)](https://docs.docker.com/reference/compose-file/services/#ports)
- [Docker docs: Pin image versions](https://docs.docker.com/build/building/best-practices/#pin-base-image-versions)
- [Prometheus v3.15.0 release](https://github.com/prometheus/prometheus/releases/tag/v3.15.0)
- [Grafana v13.2.4 release](https://github.com/grafana/grafana/releases/tag/v13.2.4)

**Slide 13**  
- [Prometheus docs: Exposition formats](https://prometheus.io/docs/instrumenting/exposition_formats/)
- [Prometheus docs: up metric](https://prometheus.io/docs/concepts/jobs_instances/#automatically-generated-labels-and-time-series)

**Slide 15**  
- [Prometheus docs: Overview (pull model)](https://prometheus.io/docs/introduction/overview/)
- [Prometheus docs: When to use the Pushgateway](https://prometheus.io/docs/practices/pushing/)
- [Prometheus docs: up metric](https://prometheus.io/docs/concepts/jobs_instances/#automatically-generated-labels-and-time-series)

**Slide 16**  
- [Prometheus docs: Storage](https://prometheus.io/docs/prometheus/latest/storage/#local-storage)
- [Prometheus docs: Alerting rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/)
- [Prometheus docs: Recording rules](https://prometheus.io/docs/practices/rules/)
- [Prometheus docs: Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [Thanos: Quick tutorial](https://thanos.io/tip/thanos/quick-tutorial.md/)
- [Grafana Mimir: HA deduplication](https://grafana.com/docs/mimir/latest/configure/configure-high-availability-deduplication/)

**Slide 17**  
- [Prometheus docs: Configuration (defaults)](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#configuration-file)
- [Prometheus docs: kubernetes_sd_config](https://prometheus.io/docs/prometheus/latest/configuration/configuration/#kubernetes_sd_config)
- [Prometheus Operator: Introduction](https://prometheus-operator.dev/docs/getting-started/introduction/)
- [Docker docs: Networking in Compose](https://docs.docker.com/compose/how-tos/networking/)

**Slide 18**  
- [Prometheus docs: up metric](https://prometheus.io/docs/concepts/jobs_instances/#automatically-generated-labels-and-time-series)

**Slide 19**  
- [Prometheus docs: Data model](https://prometheus.io/docs/concepts/data_model/)

**Slide 20**  
- [Prometheus docs: Metric types](https://prometheus.io/docs/concepts/metric_types/)
- [Prometheus docs: Histograms and summaries](https://prometheus.io/docs/practices/histograms/#quantiles)
- [Prometheus docs: Native histograms](https://prometheus.io/docs/specs/native_histograms/)

**Slide 21**  
- [prometheus_client (Python): Histogram](https://prometheus.github.io/client_python/instrumenting/histogram/)

**Slide 22**  
- [Prometheus docs: Naming, labels](https://prometheus.io/docs/practices/naming/#labels)
- [Prometheus docs: Do not overuse labels](https://prometheus.io/docs/practices/instrumentation/#do-not-overuse-labels)
- [Prometheus docs: Aggregation operators (topk, count)](https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators)

**Slide 23**  
- [Prometheus docs: rate()](https://prometheus.io/docs/prometheus/latest/querying/functions/#rate)
- [Prometheus docs: irate()](https://prometheus.io/docs/prometheus/latest/querying/functions/#irate)
- [Prometheus docs: increase()](https://prometheus.io/docs/prometheus/latest/querying/functions/#increase)
- [Grafana docs: $__rate_interval](https://grafana.com/docs/grafana/latest/datasources/prometheus/template-variables/#use-__rate_interval)

**Slide 24**  
- [Prometheus docs: Regular expressions](https://prometheus.io/docs/prometheus/latest/querying/basics/#regular-expressions)
- [Prometheus docs: Aggregation operators](https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators)

**Slide 25**  
- [Prometheus docs: histogram_quantile()](https://prometheus.io/docs/prometheus/latest/querying/functions/#histogram_quantile)
- [Prometheus docs: Errors of quantile estimation](https://prometheus.io/docs/practices/histograms/#errors-of-quantile-estimation)

**Slide 26**  
- [Prometheus docs: increase()](https://prometheus.io/docs/prometheus/latest/querying/functions/#increase)
- [Prometheus docs: Aggregation operators (topk)](https://prometheus.io/docs/prometheus/latest/querying/operators/#aggregation-operators)

**Slide 29**  
- [Grafana docs: Data sources](https://grafana.com/docs/grafana/latest/datasources/)
- [Grafana plugin catalog: data sources](https://grafana.com/grafana/plugins/?type=datasource)
- [Grafana docs: Visualizations](https://grafana.com/docs/grafana/latest/panels-visualizations/visualizations/)
- [Grafana docs: Alerting fundamentals](https://grafana.com/docs/grafana/latest/alerting/fundamentals/)
- [Grafana docs: Provisioning](https://grafana.com/docs/grafana/latest/administration/provisioning/)

**Slide 30**  
- [Tom Wilkie: The RED Method](https://grafana.com/blog/2018/08/02/the-red-method-how-to-instrument-your-services/)
- [Brendan Gregg: The USE Method](https://www.brendangregg.com/usemethod.html)
- [Google SRE book: Four golden signals](https://sre.google/sre-book/monitoring-distributed-systems/#xref_monitoring_golden-signals)

**Slide 31**  
- [Grafana docs: Prometheus query editor (legend)](https://grafana.com/docs/grafana/latest/datasources/prometheus/query-editor/)
- [Grafana docs: Standard options (units)](https://grafana.com/docs/grafana/latest/panels-visualizations/configure-standard-options/)

**Slide 32**  
- [Grafana docs: Prometheus template variables](https://grafana.com/docs/grafana/latest/datasources/prometheus/template-variables/)
- [Grafana docs: Multi-value variables](https://grafana.com/docs/grafana/latest/dashboards/variables/add-template-variables/#multi-value-variables)

**Slide 33**  
- [Grafana docs: Provisioning dashboards](https://grafana.com/docs/grafana/latest/administration/provisioning/#dashboards)
- [Grafana docs: Export a dashboard as code](https://grafana.com/docs/grafana/latest/dashboards/share-dashboards-panels/#export-a-dashboard-as-code)
- [Grafana Foundation SDK](https://grafana.github.io/grafana-foundation-sdk/)
- [Grafana Terraform provider](https://github.com/grafana/terraform-provider-grafana)
- [Grafonnet](https://github.com/grafana/grafonnet)

**Slide 35**  
- [Prometheus docs: Alerting rules (for)](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/#defining-alerting-rules)
- [Prometheus docs: Inspecting alerts](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/#inspecting-alerts-during-runtime)

**Slide 36**  
- [Prometheus docs: Alerting rules](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/#defining-alerting-rules)
- [Prometheus docs: Alertmanager](https://prometheus.io/docs/alerting/latest/alertmanager/)

**Slide 37**  
- [Google SRE book: Symptoms vs causes](https://sre.google/sre-book/monitoring-distributed-systems/)
- [Google SRE workbook: Multiwindow, multi-burn-rate alerts](https://sre.google/workbook/alerting-on-slos/#6-multiwindow-multi-burn-rate-alerts)
- [Grafana Cloud docs: SLO burn-rate alerts](https://grafana.com/docs/grafana-cloud/observe-and-act/alert-and-measure-reliability/slo/set-up/configure-burn-rate-notifications/)
- [Sloth](https://github.com/slok/sloth)

**Slide 38**  
- [Prometheus docs: Alerting rules (for)](https://prometheus.io/docs/prometheus/latest/configuration/alerting_rules/#defining-alerting-rules)
- [Prometheus docs: rate()](https://prometheus.io/docs/prometheus/latest/querying/functions/#rate)

**Slide 41**  
- [MCP: What is the Model Context Protocol?](https://modelcontextprotocol.io/docs/getting-started/intro)
- [MCP spec: Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- [grafana/mcp-grafana v2.0.2 README](https://github.com/grafana/mcp-grafana/blob/v2.0.2/README.md)
- [Claude Code docs: MCP](https://code.claude.com/docs/en/mcp)
- [Cursor docs: MCP](https://cursor.com/docs/context/mcp)

**Slide 42**  
- [grafana/mcp-grafana v2.0.2 README](https://github.com/grafana/mcp-grafana/blob/v2.0.2/README.md)

**Slide 43**  
- [Grafana docs: Service accounts](https://grafana.com/docs/grafana/latest/administration/service-accounts/)
- [grafana/mcp-grafana v2.0.2 README (flags)](https://github.com/grafana/mcp-grafana/blob/v2.0.2/README.md)
- [grafana/mcp-grafana v2.0.2 Dockerfile (SSE default)](https://github.com/grafana/mcp-grafana/blob/v2.0.2/Dockerfile)
- [MCP spec: Transports](https://modelcontextprotocol.io/specification/2025-06-18/basic/transports)

**Slide 45**  
- [Kubernetes: kind quick start](https://kind.sigs.k8s.io/docs/user/quick-start/)
- [Loki docs: LogQL](https://grafana.com/docs/loki/latest/query/)
- [OpenTelemetry: What is OpenTelemetry?](https://opentelemetry.io/docs/what-is-opentelemetry/)
- [Thanos: Quick tutorial](https://thanos.io/tip/thanos/quick-tutorial.md/)
- [Grafana Mimir: HA deduplication](https://grafana.com/docs/mimir/latest/configure/configure-high-availability-deduplication/)
- [Google SRE workbook: Alerting on SLOs](https://sre.google/workbook/alerting-on-slos/)

## Meme templates

- Gru's Plan: [imgflip](https://imgflip.com/memetemplate/131940431/Grus-Plan) · [Know Your Meme](https://knowyourmeme.com/memes/grus-plan)
- Left Exit 12 Off Ramp: [imgflip](https://imgflip.com/memetemplate/124822590/Left-Exit-12-Off-Ramp) · [Know Your Meme](https://knowyourmeme.com/memes/left-exit-12-off-ramp)
- Is This A Pigeon: [imgflip](https://imgflip.com/memetemplate/100777631/Is-This-A-Pigeon) · [Know Your Meme](https://knowyourmeme.com/memes/is-this-a-pigeon)
- Success Kid: [imgflip](https://imgflip.com/memetemplate/61544/Success-Kid) · [Know Your Meme](https://knowyourmeme.com/memes/success-kid-i-hate-sandcastles)
