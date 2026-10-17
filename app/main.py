"""checkout-api — the service we instrument, scrape, graph and break in the workshop.

Endpoints:  GET /products   POST /checkout   GET /healthz   GET /metrics   GET|POST /chaos
"""
import asyncio
import json
import random
import time
import uuid
from typing import Literal

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import CONTENT_TYPE_LATEST, Counter, Gauge, Histogram, generate_latest
from pydantic import BaseModel, Field, ValidationError
from starlette.routing import Match

# ── Metrics ────────────────────────────────────────────────────────────────
# These names are used verbatim by the slides, the dashboard, the alert rules
# and the exercises. Rename one and you break all four.

REQUESTS = Counter(
    "http_requests_total", "Total HTTP requests served.", ["method", "route", "status"]
)
LATENCY = Histogram(
    "http_request_duration_seconds",
    "Time spent serving a request.",
    ["method", "route"],
    buckets=(0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)
IN_PROGRESS = Gauge(
    "http_requests_in_progress", "Requests currently being served.", ["route"]
)
ORDERS = Counter(
    "checkout_orders_total", "Orders placed successfully.", ["payment_method"]
)
CHAOS_ERROR_RATE = Gauge("chaos_error_rate", "Injected failure probability on /checkout (0-1).")
CHAOS_LATENCY = Gauge("chaos_latency_seconds", "Injected extra latency on /checkout.")

# Real systems are never perfectly green; a small baseline keeps the error panel honest.
BASE_ERROR_RATE = 0.01

PRODUCTS = [
    {"id": "vada-pav", "name": "Vada Pav", "price_inr": 25},
    {"id": "cutting-chai", "name": "Cutting Chai", "price_inr": 15},
    {"id": "misal-pav", "name": "Misal Pav", "price_inr": 90},
    {"id": "bombay-sandwich", "name": "Bombay Sandwich", "price_inr": 70},
]


def from_other_site(request: Request) -> bool:
    """curl and Grafana send no Origin header. A browser on another site does, so refuse those
    (stops a random web page from flipping your chaos switch through localhost)."""
    origin = request.headers.get("origin")
    if not origin:
        return False
    host = origin.split("://", 1)[-1].split(":", 1)[0]
    return host not in ("localhost", "127.0.0.1")


class Chaos(BaseModel):
    latency_ms: int = Field(0, ge=0, le=10_000)
    error_rate: float = Field(0.0, ge=0.0, le=1.0)


class Order(BaseModel):
    payment_method: Literal["upi", "card", "cod"] = "upi"


app = FastAPI(title="checkout-api")
app.state.chaos = Chaos()


def route_template(request: Request) -> str:
    """The route *template* (e.g. /checkout), never the raw path.

    Raw paths would turn every typo and scanner hit into a new time series.
    """
    for route in app.router.routes:
        match, _ = route.matches(request.scope)
        if match == Match.FULL:
            return route.path
    return "unmatched"


@app.middleware("http")
async def instrument(request: Request, call_next):
    route = route_template(request)
    if route == "/metrics":
        return await call_next(request)

    method = request.method
    IN_PROGRESS.labels(route).inc()
    start = time.perf_counter()
    status = "500"
    try:
        response = await call_next(request)
        status = str(response.status_code)
        return response
    finally:
        LATENCY.labels(method, route).observe(time.perf_counter() - start)
        REQUESTS.labels(method, route, status).inc()
        IN_PROGRESS.labels(route).dec()


@app.get("/products")
async def products():
    await asyncio.sleep(random.uniform(0.005, 0.04))
    return PRODUCTS


@app.post("/checkout")
async def checkout(order: Order | None = None):
    order = order or Order()
    chaos: Chaos = app.state.chaos
    await asyncio.sleep(random.uniform(0.05, 0.2) + chaos.latency_ms / 1000)
    if random.random() < max(BASE_ERROR_RATE, chaos.error_rate):
        raise HTTPException(status_code=500, detail="payment gateway timed out")
    ORDERS.labels(order.payment_method).inc()
    return {"order_id": uuid.uuid4().hex[:12], "payment_method": order.payment_method}


@app.get("/healthz")
async def healthz():
    return {"status": "ok"}


@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


@app.get("/chaos")
async def get_chaos():
    return app.state.chaos


@app.post("/chaos")
async def set_chaos(request: Request):
    """Accepts JSON with or without a content-type header; an empty body resets chaos.

    The slides use `curl -X POST localhost:8080/chaos -d '{"latency_ms":1200}'`,
    which sends no JSON content-type — so we parse the raw body ourselves.
    """
    if from_other_site(request):
        return JSONResponse(status_code=403, content={"error": "cross-site request refused"})
    raw = await request.body()
    try:
        data = json.loads(raw) if raw.strip() else {}
        if not isinstance(data, dict):
            raise ValueError("body must be a JSON object")
        chaos = Chaos(**data)
    except (ValueError, ValidationError) as exc:
        return JSONResponse(status_code=422, content={"error": str(exc)})

    app.state.chaos = chaos
    CHAOS_ERROR_RATE.set(chaos.error_rate)
    CHAOS_LATENCY.set(chaos.latency_ms / 1000)
    return chaos
