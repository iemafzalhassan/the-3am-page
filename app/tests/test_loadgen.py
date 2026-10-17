import collections

import loadgen


def test_mix_is_mostly_products():
    picks = [loadgen.pick_request() for _ in range(5000)]
    paths = collections.Counter(path for _, path, _ in picks)
    assert 0.6 < paths["/products"] / 5000 < 0.8
    assert set(paths) <= {"/products", "/checkout"}


def test_checkouts_use_valid_payment_methods():
    picks = [loadgen.pick_request() for _ in range(2000)]
    methods = {body["payment_method"] for _, path, body in picks if path == "/checkout"}
    assert methods and methods <= {"upi", "card", "cod"}


def test_http_methods_match_endpoints():
    for method, path, body in (loadgen.pick_request() for _ in range(500)):
        assert (method, path) in {("GET", "/products"), ("POST", "/checkout")}
        assert (body is None) == (path == "/products")
