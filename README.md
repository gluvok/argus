# Argus — ANPR Microservice

Reads Indian vehicle number plates from an uploaded image for weighbridge gatekeeping. Runs as a FastAPI service on a Raspberry Pi 5, CPU-only, listening on `127.0.0.1:8000`.

- **Consumers:** Hermes (same Pi) and Janus. Their integration contract is [docs/argus-spec.md](docs/argus-spec.md).
- **Contributing / AI agents:** see [CLAUDE.md](CLAUDE.md) and [AGENTS.md](AGENTS.md).

---

## How it works

Each image goes through Stage 1 **vehicle detection** with YOLO26n (OpenVINO, `yolo26n_openvino_model/`). Vehicles are sorted largest-first, then Stage 2 **plate reading** runs a 4-tier cascade. Each tier runs only if all earlier tiers found nothing:

| Tier | Engine | Input | `vehicle_box` | Approx. latency* |
|---|---|---|---|---|
| 1 | Fast-ALPR (YOLOv9-s plate detector + CCT-XS OCR, ONNX Runtime) | vehicle crops | set | ~30–50 ms |
| 2 | Fast-ALPR | full frame (covers non-COCO vehicles such as tractors) | `null` | ~30–50 ms |
| 3 | RapidOCR (OpenVINO) + 2D spatial token pairing + contrast retry | vehicle crops | set | ~120–180 ms |
| 4 | RapidOCR | full frame | `null` | ~220–280 ms |

Every candidate is normalised and validated against Indian registration rules (state codes, OCR-confusion fixes, HSRP `IND` prefix, decal and phone-number filters) in `app/services/plate_rules/`.

\* Historical figures. Measure on your hardware with `uv run python test_direct.py`.

---

## Local development

**Prerequisites:** [uv](https://docs.astral.sh/uv/) and Python 3.14 (`.python-version`). On first run, Fast-ALPR downloads its plate models to `~/.cache/open-image-models/` and `~/.cache/fast-plate-ocr/`, so you need internet once.

```bash
uv sync                                  # install runtime + dev dependencies
uv run fastapi dev                       # hot-reload server → http://localhost:8000/docs
uv run fastapi run --host 127.0.0.1      # production mode locally
```

### Configuration

Optional `.env` in the working directory (see `.env.example`):

| Variable | Default | Effect |
|---|---|---|
| `ENABLE_MULTI_VEHICLE_OCR` | `false` | `true` returns plates from every vehicle in the frame instead of stopping at the first vehicle with a match |

Thresholds, upload limits, host and port are code constants in `app/core/constants.py`.

### Checks (run before every push)

```bash
uv run ruff check --fix
uv run ty check
uv run pytest tests/ -v
```

`git config core.hooksPath .githooks` enables a pre-push hook that runs the same three. CI (`.github/workflows/ci.yml`) runs them on every PR to `main`.

---

## API

### `POST /recognize`

Multipart upload with one field, `file`: JPEG, PNG, WebP or BMP, up to 8 MB and 50 megapixels.

```bash
curl -X POST "http://127.0.0.1:8000/recognize" \
  -H "Accept: application/json" \
  -F "file=@tests/images/1.jpg"
```

`200 OK`:

```json
{
  "results": [
    { "plate": "RJ09GA0165", "vehicle_box": [10, 10, 50, 50], "execution_time_ms": 31.42 }
  ],
  "execution_time_ms": 31.42
}
```

- `plate`: uppercase, no separators.
- `vehicle_box`: `[x1, y1, x2, y2]` in image pixels, or `null` when the plate came from a full-frame tier.
- **No plate found still returns `200` with `"results": []`.**
- Every response carries an `X-Process-Time-Ms` header.

Errors use one JSON shape: `success`, `status_code`, `message`, `error_type`, `details`, `timestamp`.

| Status | `error_type` | Cause |
|---|---|---|
| 400 | `InvalidImageError` | wrong content type, empty file, unsupported or corrupt image |
| 413 | `PayloadTooLargeError` | over 8 MB or 50 megapixels |
| 422 | `RequestValidationError` | missing `file` field |
| 500 | `InternalServerError` / `ContractViolation` | engine or internal failure |

### `GET /health` and `GET /`

```bash
curl http://127.0.0.1:8000/health
# {"status":"healthy","service":"Argus ANPR Microservice","version":"dev"}
```

`/health` is static. It doesn't confirm that the models loaded, so use a real `/recognize` call as a readiness check. `version` reports `"dev"` because the project isn't installed as a package.

`GET /` returns name, version, status and a link to `/docs`.

---

## Deploying to the Raspberry Pi 5

```bash
uv run python scripts/deploy.py --dry-run                   # print every command
uv run python scripts/deploy.py --host gluvok@hermes.local  # deploy
```

The script makes four SSH passes to the Pi:

1. Prepare `/opt/argus`.
2. `rsync` the repo, including the model weights in `yolo26n_openvino_model/`.
3. Run `uv sync` and compile `app/` with Nuitka into a native extension (`app.*.so`), then **delete all `.py` source** from the device.
4. Install and restart `argus.service`, which binds `127.0.0.1:8000` with `Restart=always`.

Full details are in [docs/argus-spec.md §6](docs/argus-spec.md#6-edge-deployment-raspberry-pi-5).

Separately, merges to `main` trigger `.github/workflows/nuitka.yml`. It builds the same `.so` for arm64 and force-pushes it to the `release` branch.

On the Pi:

```bash
systemctl status argus
journalctl -u argus -f
```

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| `/health` is fine but `/recognize` returns 500 | Fast-ALPR models failed to download on first start | Give the Pi internet once and restart the service, or pre-seed `~/.cache/open-image-models` and `~/.cache/fast-plate-ocr` for the service user |
| `200` with `results: []` on a clear plate | Plate format not supported (e.g. BH-series), or the text was filtered as a decal | Check the `[pipeline] Tier N` log lines; adjust `app/services/plate_rules/` |
| Requests queue up under load | Only 4 inferences run at once (`MAX_CONCURRENT_INFERENCES`) | Send one request per camera trigger; set a client timeout |
| Can't reach the service from another machine | Bound to loopback by design | Call it from the same host |
