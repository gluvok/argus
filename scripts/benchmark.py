"""Sequential /recognize latency benchmark (inference is serialised by _inference_lock)."""

import argparse
import math
import time

import httpx

p = argparse.ArgumentParser()
p.add_argument("--url", default="http://127.0.0.1:8000/recognize")
p.add_argument("--image", default="tests/images/8.jpg", help="JPEG to send")
p.add_argument("-n", type=int, default=50)
p.add_argument("--warmup", type=int, default=3)
a = p.parse_args()

with open(a.image, "rb") as f:
    frame = f.read()
lat, errors = [], 0
with httpx.Client(timeout=120) as c:
    for i in range(a.warmup + a.n):
        t0 = time.perf_counter()
        try:
            ok = c.post(a.url, files={"file": ("frame.jpg", frame, "image/jpeg")}).status_code == 200
        except httpx.HTTPError:
            ok = False
        dt = (time.perf_counter() - t0) * 1000
        if i < a.warmup:
            continue
        if ok:
            lat.append(dt)
        else:
            errors += 1

if not lat:
    raise SystemExit(f"no successful requests ({errors} errors)")
lat.sort()
p95 = lat[math.ceil(0.95 * len(lat)) - 1]  # nearest-rank, correct for small n
print(  # noqa: T201
    f"n={a.n} errors={errors} p50={lat[(len(lat) - 1) // 2]:.0f}ms "
    f"p95={p95:.0f}ms max={lat[-1]:.0f}ms\n"
    f"suggested ANPR_SERVER_TIMEOUT ≈ {math.ceil(p95 * 3 / 1000)} s"
)
