"""
GA4 Measurement Protocol - Checkout Funnel Event Simulator
------------------------------------------------------------
Sends realistic session_start -> view_item -> add_to_cart ->
begin_checkout -> add_payment_info -> purchase funnel events
into YOUR OWN GA4 property for today.

Run this once now to test the pipeline, then run it daily
(manually, or later via a scheduled task / UiPath) to build up
a real day-by-day dataset in your own property.

FIXED VERSION:
- Uses a reusable requests.Session() with connection pooling and
  automatic retries, which fixes the
  "ConnectionError: Remote end closed connection without response"
  error that happens when opening hundreds of fresh connections
  back-to-back.
- Added a timeout so a single hung request can't stall the script.
- Added try/except around each send_event call so a single failed
  event just gets logged and skipped, instead of crashing the
  entire 200-session run.
"""

import requests
import uuid
import time
import random
from requests.adapters import HTTPAdapter, Retry

# ---- YOUR CREDENTIALS ----
MEASUREMENT_ID = "G-MCL77P1W9L"
API_SECRET = "UhvXjPBsTTa4pk2UwYboqQ"

URL = f"https://www.google-analytics.com/mp/collect?measurement_id={MEASUREMENT_ID}&api_secret={API_SECRET}"

# --- Reusable session with retry logic (fixes the ConnectionError) ---
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries, pool_connections=10, pool_maxsize=10))


def send_event(client_id, event_name, timestamp_micros=None):
    payload = {
        "client_id": client_id,
        "events": [{"name": event_name, "params": {"engagement_time_msec": "100"}}]
    }
    if timestamp_micros:
        payload["timestamp_micros"] = timestamp_micros

    try:
        resp = session.post(URL, json=payload, timeout=10)
        return resp.status_code
    except requests.exceptions.RequestException as e:
        print(f"  [warn] failed to send '{event_name}' for {client_id[:8]}: {e}")
        return None


def simulate_funnel(num_sessions=200):
    """
    Simulates num_sessions users going through the funnel today,
    with realistic drop-off at each stage (roughly matching your
    demo account's ~78% / 75% / 55% / 31% / 32% drop-off pattern).
    """
    counts = {
        "session_start": 0,
        "view_item": 0,
        "add_to_cart": 0,
        "begin_checkout": 0,
        "add_payment_info": 0,
        "purchase": 0
    }

    # Approx retention rates from your demo account funnel
    retention = {
        "session_start": 1.0,
        "view_item": 0.215,
        "add_to_cart": 0.25,
        "begin_checkout": 0.45,
        "add_payment_info": 0.69,
        "purchase": 0.68
    }

    steps = list(retention.keys())

    for i in range(num_sessions):
        client_id = str(uuid.uuid4())
        still_active = True
        for step in steps:
            if not still_active:
                break
            # roll the dice based on retention rate for this step
            if random.random() <= retention[step] or step == "session_start":
                send_event(client_id, step)
                counts[step] += 1
                time.sleep(0.05)  # be gentle on the API
            else:
                still_active = False

    print("Sent events for", num_sessions, "simulated sessions:")
    for k, v in counts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    simulate_funnel(num_sessions=200)
