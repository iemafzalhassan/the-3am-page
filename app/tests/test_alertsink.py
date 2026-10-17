from fastapi.testclient import TestClient

import alertsink

client = TestClient(alertsink.app)


def test_alertsink_shows_firing_alert():
    body = {
        "status": "firing",
        "alerts": [{
            "status": "firing",
            "labels": {"alertname": "CheckoutP99High", "severity": "page"},
            "annotations": {"summary": "Checkout p99 is above 1s"},
            "startsAt": "2026-10-17T11:47:00Z",
        }],
    }
    assert client.post("/alerts", json=body).status_code == 200
    page = client.get("/").text
    assert "CheckoutP99High" in page
    assert "Checkout p99 is above 1s" in page


def test_alertsink_tolerates_partial_payload():
    assert client.post("/alerts", json={"alerts": [{}]}).status_code == 200
    assert client.post("/alerts", json={}).status_code == 200
    assert client.post("/alerts", content=b"garbage").status_code == 400
    assert client.get("/").status_code == 200


def test_alertsink_escapes_html():
    body = {"alerts": [{"labels": {"alertname": "<script>x</script>"}}]}
    client.post("/alerts", json=body)
    page = client.get("/").text
    assert "<script>x</script>" not in page
    assert "&lt;script&gt;" in page


def test_alertsink_survives_non_string_fields():
    body = {"alerts": [{"status": 1, "labels": {"alertname": 42}, "annotations": ["not", "a", "dict"]}]}
    assert client.post("/alerts", json=body).status_code == 200
    assert client.get("/").status_code == 200


def test_alertsink_refuses_cross_site_posts():
    r = client.post("/alerts", json={"alerts": []}, headers={"origin": "https://evil.example"})
    assert r.status_code == 403
