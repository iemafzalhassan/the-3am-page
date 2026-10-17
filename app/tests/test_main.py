from fastapi.testclient import TestClient
from prometheus_client import REGISTRY

import main

client = TestClient(main.app)


def val(name, **labels):
    return REGISTRY.get_sample_value(name, labels) or 0.0


def setup_function():
    client.post("/chaos", content=b"")
    main.BASE_ERROR_RATE = 0.0


def test_products_counted_with_route_template():
    before = val("http_requests_total", method="GET", route="/products", status="200")
    assert client.get("/products").status_code == 200
    assert val("http_requests_total", method="GET", route="/products", status="200") == before + 1


def test_latency_histogram_has_workshop_buckets():
    client.get("/products")
    for le in ("0.025", "0.05", "0.1", "0.25", "0.5", "1.0", "2.5", "5.0", "+Inf"):
        assert REGISTRY.get_sample_value(
            "http_request_duration_seconds_bucket", {"method": "GET", "route": "/products", "le": le}
        ) is not None


def test_unknown_path_is_labelled_unmatched():
    client.get("/wp-admin/setup.php")
    assert val("http_requests_total", method="GET", route="unmatched", status="404") >= 1
    assert REGISTRY.get_sample_value(
        "http_requests_total", {"method": "GET", "route": "/wp-admin/setup.php", "status": "404"}
    ) is None


def test_metrics_endpoint_is_not_self_counted():
    client.get("/metrics")
    assert REGISTRY.get_sample_value(
        "http_requests_total", {"method": "GET", "route": "/metrics", "status": "200"}
    ) is None


def test_chaos_accepts_body_without_content_type():
    r = client.post("/chaos", content=b'{"latency_ms": 200}')
    assert r.status_code == 200
    assert r.json()["latency_ms"] == 200
    assert val("chaos_latency_seconds") == 0.2


def test_chaos_rejects_out_of_range_and_keeps_old_state():
    client.post("/chaos", content=b'{"error_rate": 0.1}')
    assert client.post("/chaos", content=b'{"error_rate": 5}').status_code == 422
    assert client.post("/chaos", content=b'{"latency_ms": -1}').status_code == 422
    assert client.post("/chaos", content=b"not json").status_code == 422
    assert client.post("/chaos", content=b"[1, 2]").status_code == 422
    assert client.get("/chaos").json()["error_rate"] == 0.1
    assert val("chaos_error_rate") == 0.1


def test_empty_body_resets_chaos():
    client.post("/chaos", content=b'{"error_rate": 0.5, "latency_ms": 900}')
    assert client.post("/chaos", content=b"").json() == {"latency_ms": 0, "error_rate": 0.0}
    assert val("chaos_error_rate") == 0.0
    assert val("chaos_latency_seconds") == 0.0


def test_checkout_fails_under_full_error_chaos():
    client.post("/chaos", content=b'{"error_rate": 1}')
    before = val("http_requests_total", method="POST", route="/checkout", status="500")
    assert client.post("/checkout", json={"payment_method": "upi"}).status_code == 500
    assert val("http_requests_total", method="POST", route="/checkout", status="500") == before + 1


def test_checkout_counts_orders_by_payment_method():
    before = val("checkout_orders_total", payment_method="card")
    assert client.post("/checkout", json={"payment_method": "card"}).status_code == 200
    assert val("checkout_orders_total", payment_method="card") == before + 1


def test_checkout_without_body_defaults_to_upi():
    before = val("checkout_orders_total", payment_method="upi")
    assert client.post("/checkout").status_code == 200
    assert val("checkout_orders_total", payment_method="upi") == before + 1


def test_unknown_payment_method_rejected():
    assert client.post("/checkout", json={"payment_method": "bitcoin"}).status_code == 422


def test_chaos_latency_slows_checkout_only():
    client.post("/chaos", content=b'{"latency_ms": 300}')
    before = val("http_request_duration_seconds_sum", method="POST", route="/checkout")
    client.post("/checkout", json={"payment_method": "upi"})
    assert val("http_request_duration_seconds_sum", method="POST", route="/checkout") - before >= 0.3


def test_chaos_refuses_cross_site_browser_posts():
    r = client.post("/chaos", content=b'{"error_rate": 1}', headers={"origin": "https://evil.example"})
    assert r.status_code == 403
    assert client.get("/chaos").json()["error_rate"] == 0.0


def test_chaos_allows_local_browser_origin():
    r = client.post("/chaos", content=b'{"latency_ms": 10}', headers={"origin": "http://localhost:3000"})
    assert r.status_code == 200
