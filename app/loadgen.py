"""loadgen — steady background traffic so every graph has something to show.

Same image as checkout-api, different command:  python loadgen.py
Env:  TARGET (default http://checkout-api:8080)   RPS (default 10)
"""
import asyncio
import logging
import os
import random

import httpx

TARGET = os.environ.get("TARGET", "http://checkout-api:8080")
RPS = float(os.environ.get("RPS", "10"))

log = logging.getLogger("loadgen")

# Roughly what a food-ordering app looks like: lots of browsing, some buying,
# and in Mumbai most people pay with UPI.
PAYMENT_METHODS = ["upi", "card", "cod"]
PAYMENT_WEIGHTS = [0.6, 0.3, 0.1]
CHECKOUT_SHARE = 0.3


def pick_request() -> tuple[str, str, dict | None]:
    """Return (http_method, path, json_body) for the next request."""
    if random.random() < CHECKOUT_SHARE:
        method = random.choices(PAYMENT_METHODS, PAYMENT_WEIGHTS)[0]
        return "POST", "/checkout", {"payment_method": method}
    return "GET", "/products", None


async def fire(client: httpx.AsyncClient, gate: asyncio.Semaphore) -> None:
    async with gate:
        method, path, body = pick_request()
        try:
            await client.request(method, path, json=body)
        except httpx.HTTPError as exc:
            log.warning("%s %s failed: %s", method, path, exc)


async def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s loadgen %(message)s")
    log.info("sending ~%s req/s to %s", RPS, TARGET)
    # Fire-and-forget under a semaphore: slow checkouts (chaos!) must not lower the
    # request rate, otherwise the Rate panel would dip exactly when latency spikes.
    gate = asyncio.Semaphore(50)
    tasks: set[asyncio.Task] = set()
    async with httpx.AsyncClient(base_url=TARGET, timeout=15) as client:
        while True:
            task = asyncio.create_task(fire(client, gate))
            tasks.add(task)
            task.add_done_callback(tasks.discard)
            await asyncio.sleep(1 / RPS)


if __name__ == "__main__":
    asyncio.run(main())
