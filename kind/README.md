# Open-lab bonus: the same stack on Kubernetes (kind)

Same app, same metrics, same PromQL — but now Prometheus **discovers pods** instead of a static target,
and there are **two replicas**, so `sum by (…)` suddenly matters.

Needs: [kind](https://kind.sigs.k8s.io/docs/user/quick-start/#installation), kubectl, ~2.5 GB free memory.
Stop the compose stack first: `docker compose down`.

```bash
kind create cluster --config kind/kind-config.yaml
docker compose build checkout-api                       # or load the pen-drive images
kind load docker-image ghcr.io/iemafzalhassan/checkout-api:1.0 prom/prometheus:v3.15.0 grafana/grafana:13.2.4 --name the-3am-page
kubectl apply -f kind/app.yaml -f kind/monitoring.yaml
kubectl wait --for=condition=Available deploy --all --timeout=180s
```

| What | Where |
|---|---|
| checkout-api | http://localhost:18080/products |
| Prometheus | http://localhost:19090/targets — **two** targets, one per pod |
| Grafana | http://localhost:13000 (admin / admin) — import `grafana/dashboards/checkout-red.json` |

Try:

```promql
sum by (pod) (rate(http_requests_total[1m]))      # load split across replicas
sum(rate(http_requests_total[1m]))                # the service as a whole
```

**Puzzle:** one pod gets almost all the traffic. Why? The load generator keeps its HTTP connections
alive and, at ~10 req/s, reuses just one or a few of them. A Kubernetes Service balances *connections*, not *requests*. Same reason gRPC
needs client-side or L7 (service mesh) load balancing. Fix it for fun: `kubectl scale deploy loadgen --replicas=3`.

Then kill a pod and watch `up`: `kubectl delete pod -l app=checkout-api --wait=false`

Clean up: `kind delete cluster --name the-3am-page`

Going further: the [Prometheus Operator](https://prometheus-operator.dev/) replaces the hand-written
`kubernetes_sd_configs` with a `ServiceMonitor` CRD; `kube-prometheus-stack` (Helm) bundles it all.
