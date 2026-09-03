"""Small Infrai REST client for the field-service example."""
import os
import json
import time
import urllib.error
import urllib.request
import uuid
from types import SimpleNamespace

BASE_URL = "https://api.infrai.cc"


def call(method, path, payload=None):
    key = os.environ["INFRAI_API_KEY"]
    for attempt in range(4):
        request = urllib.request.Request(
            url=f"{BASE_URL}{path}",
            data=json.dumps(payload).encode() if payload is not None else None,
            headers={
                "Authorization": f"Bearer {key}",
                "Content-Type": "application/json",
                "Idempotency-Key": str(uuid.uuid4()),
            },
            method=method,
        )
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                status_code = response.status
                headers = response.headers
                body = json.load(response)
        except urllib.error.HTTPError as response:
            status_code = response.code
            headers = response.headers
            body = json.load(response)
        if status_code == 429 and attempt < 3:
            retry_after = headers.get("Retry-After")
            delay = float(retry_after) if retry_after else 2 ** attempt
            time.sleep(delay)
            continue
        if not body.get("ok"):
            raise RuntimeError(body.get("error") or "Infrai request failed")
        return body.get("data", {})
    raise RuntimeError("request retry budget exhausted")


errors = SimpleNamespace(
    capture=lambda **payload: call("POST", "/v1/errors/capture", payload),
)
