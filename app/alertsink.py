"""alert-sink — a local landing page for Grafana webhook alerts (no Slack, no internet).

Same image as checkout-api, different command:
    uvicorn alertsink:app --host 0.0.0.0 --port 5001
Grafana contact point URL:  http://alert-sink:5001/alerts
"""
import html
import json
from collections import deque
from datetime import datetime, timezone

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="alert-sink")
RECEIVED: deque = deque(maxlen=50)


@app.post("/alerts")
async def receive(request: Request):
    origin = request.headers.get("origin", "")
    if origin and origin.split("://", 1)[-1].split(":", 1)[0] not in ("localhost", "127.0.0.1"):
        return JSONResponse(status_code=403, content={"error": "cross-site request refused"})
    try:
        payload = json.loads(await request.body() or b"{}")
        if not isinstance(payload, dict):
            raise ValueError("payload must be a JSON object")
    except ValueError as exc:
        return JSONResponse(status_code=400, content={"error": str(exc)})

    received_at = datetime.now(timezone.utc).strftime("%H:%M:%S UTC")
    for alert in payload.get("alerts") or []:
        if not isinstance(alert, dict):
            continue
        labels = alert.get("labels") if isinstance(alert.get("labels"), dict) else {}
        annotations = alert.get("annotations") if isinstance(alert.get("annotations"), dict) else {}
        # str() everything: one odd payload must not break the page for everyone after it
        RECEIVED.appendleft({
            "received": received_at,
            "status": str(alert.get("status") or payload.get("status") or "unknown"),
            "name": str(labels.get("alertname", "(no alertname)")),
            "severity": str(labels.get("severity", "")),
            "summary": str(annotations.get("summary", "")),
            "starts": str(alert.get("startsAt", "")),
        })
    return {"ok": True, "stored": len(RECEIVED)}


PAGE = """<!doctype html><html><head><meta charset="utf-8">
<meta http-equiv="refresh" content="5"><title>alert-sink</title>
<style>
body{{background:#111217;color:#E6E7EA;font:16px/1.5 system-ui,sans-serif;margin:40px}}
h1{{font-weight:700;letter-spacing:-.02em}} small{{color:#9A9CA5}}
table{{border-collapse:collapse;width:100%;margin-top:24px}}
td,th{{text-align:left;padding:12px 16px;border-bottom:1px solid #2A2D35}}
th{{color:#9A9CA5;font-weight:500;font-size:13px;text-transform:uppercase;letter-spacing:.08em}}
.firing{{color:#F2495C;font-weight:700}} .resolved{{color:#73BF69;font-weight:700}}
.empty{{color:#5C5F69;padding:40px 0}}
</style></head><body>
<h1>alert-sink <small>· Grafana webhooks land here · refreshes every 5s</small></h1>
{body}
</body></html>"""


@app.get("/", response_class=HTMLResponse)
async def page():
    if not RECEIVED:
        return PAGE.format(body='<p class="empty">No alerts yet. Break something: '
                                '<code>curl -X POST localhost:8080/chaos -d \'{"latency_ms":1200}\'</code></p>')
    rows = "".join(
        f'<tr><td>{html.escape(a["received"])}</td>'
        f'<td class="{html.escape(a["status"])}">{html.escape(a["status"].upper())}</td>'
        f'<td>{html.escape(a["name"])}</td><td>{html.escape(a["severity"])}</td>'
        f'<td>{html.escape(a["summary"])}</td><td>{html.escape(a["starts"])}</td></tr>'
        for a in RECEIVED
    )
    head = "<tr><th>received</th><th>status</th><th>alert</th><th>severity</th><th>summary</th><th>started</th></tr>"
    return PAGE.format(body=f"<table>{head}{rows}</table>")
