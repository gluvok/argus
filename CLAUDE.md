# Argus — Developer & Agent Guide

ANPR (Indian number plate) microservice for weighbridge gatekeeping. One FastAPI process, CPU-only inference, deployed as a Nuitka-compiled `.so` on a Raspberry Pi 5 bound to `127.0.0.1:8000`. Behavioural rules for agents live in [AGENTS.md](AGENTS.md) (think first, surgical diffs, verification loop) — they apply here too. The integration contract for Hermes/Janus lives in [docs/argus-spec.md](docs/argus-spec.md).

## Stack (only what shapes the code)

| Concern | Choice | Where |
|---|---|---|
| Runtime | Python `>=3.14` (`.python-version` = `3.14`), `uv` | `pyproject.toml`, `uv.lock` |
| HTTP | `fastapi[standard]`; entrypoint `app.server:app` via `[tool.fastapi]` | `app/server.py` |
| Vehicle detector | `ultralytics` YOLO26n, OpenVINO IR export, COCO classes | `yolo26n_openvino_model/` (git-tracked) |
| Plate engine (primary) | `fast-alpr[onnx]` on `onnxruntime`: `yolo-v9-s-608-license-plate-end2end` + `cct-xs-v2-global-model` | `app/services/ocr/fast_alpr/` |
| Plate engine (fallback) | `rapidocr` with Det/Cls/Rec on OpenVINO, 4 threads | `app/services/ocr/rapidocr/` |
| Config | `pydantic-settings`, reads `.env` from CWD; one flag: `ENABLE_MULTI_VEHICLE_OCR` (default `false`) | `app/core/config.py`, `.env.example` |
| Tunables | Plain module constants (thresholds, limits, host/port) — not env-driven | `app/core/constants.py` |
| Logging | `loguru` re-exported as `app.core.logging.logger` | |
| Dev tooling | `ruff` (adds `T20` no-print, `FAST`), `ty`, `pytest` + `pytest-cov`, `nuitka` | `[dependency-groups].dev` |

## Commands

```bash
uv sync                                   # install runtime + dev groups
uv run fastapi dev                        # hot-reload dev server, docs at http://localhost:8000/docs
uv run fastapi run --host 127.0.0.1       # prod-mode locally
uv run pytest tests/ -v                   # full suite (loads real models; slow first run)
uv run ruff check --fix && uv run ty check && uv run pytest   # required loop before commit/push (AGENTS.md §5)
uv run python test_direct.py              # accuracy/latency benchmark over tests/images → benchmark_report.md
uv run python scripts/deploy.py --dry-run # print the Pi deploy commands
uv run python scripts/deploy.py --host gluvok@hermes.local
git config core.hooksPath .githooks       # enable .githooks/pre-push (ruff → ty → pytest)
```

## Layout

```
app/server.py              create_app(): lifespan → middleware → exception handlers → routes
app/api/routes/            info.py (GET /, GET /health), recognition.py (POST /recognize)
app/api/errors.py          exception → APIErrorResponse mapping
app/api/dependencies.py    process-wide asyncio.Semaphore(MAX_CONCURRENT_INFERENCES=4)
app/core/                  constants, config, exceptions, contracts (require/ensure), bounds, lifespan, middleware
app/schemas.py             internal dataclasses (OCRToken, PlateCandidate, DetectedVehicle) + API models
app/services/image_processing/  upload validation (security.py), decode + pixel guard (transformer.py, loader.py)
app/services/detector/     Stage 1: YOLO26 vehicle detection, clamp/dedup/sort
app/services/ocr/          Stage 2: strategies/ (FastALPROCREngine, RapidOCREngine), spatial/ (RapidOCR token pairing)
app/services/pipeline/     orchestrator.py = the 4-tier cascade; response.py builds the response
app/services/plate_rules/  Indian plate normalisation + validation (specification pattern in specs/)
scripts/                   deploy.py (driver) + deploy_commands.py (pure, unit-tested command templates)
```

## Request path in one breath

`POST /recognize` → `file.read()` → `validate_image_upload` (MIME + 8 MB + format) → semaphore → `asyncify(recognize_plate_image)` in a worker thread → `decode_image` (≤50 MP, EXIF-oriented RGB) → `_execute_cascade` → `_build_response`.

Cascade (`app/services/pipeline/orchestrator.py`), each tier runs only if all earlier tiers returned nothing:
1. Fast-ALPR on vehicle crops (largest box first) — `vehicle_box` set.
2. Fast-ALPR on the full frame — `vehicle_box = null`; **returns immediately** on a hit.
3. RapidOCR + spatial pairing on vehicle crops (with CLAHE contrast retry) — `vehicle_box` set.
4. RapidOCR on the full frame — `vehicle_box = null`.

Crop scans stop at the first vehicle that yields a plate unless `ENABLE_MULTI_VEHICLE_OCR=true`.

## Conventions & invariants

- **Model singletons are lazy, double-checked-locked class/module globals** (`VehicleDetector._model`, `_alpr_instance`, `_rapidocr_instance`). YOLO and RapidOCR inference also run under a `threading.Lock`; Fast-ALPR inference is unlocked. Concurrency is bounded only by the semaphore — don't remove it.
- **Patch points for tests:** the orchestrator resolves `pl.VehicleDetector` / `pl.PlateRecognizer` through `app.services.pipeline` at call time, and `VehicleDetector.get_model` goes through `app.services.detector.YOLO`. Mock there, not at the defining module.
- **Errors:** raise `InvalidImageError` (400) / `ANPRServiceError` (500) from services; use `require`/`ensure` for invariants (→ 500 `ContractViolation`). RapidOCR tiers swallow engine errors and fall through; Fast-ALPR tiers do **not** — an exception there becomes a 500.
- **Warm-up failures are non-fatal** (`app/core/lifespan.py`): the server starts and `/health` still says `healthy` even if a model failed to load. `/health` is static.
- **No-plate is success:** `200` with `"results": []`.
- `constants.VERSION` reports `"dev"` at runtime: there's no `[build-system]`, so `uv sync` never installs `argus` as a distribution for `importlib.metadata` to find.
- `app/core/constants.py` sets `YOLO_CONFIG_DIR=.cache/ultralytics` and `CI=true` at import time (isolates Ultralytics settings/telemetry). Importing it has side effects.
- Plate output is always uppercase alphanumerics, no separators (e.g. `RJ09GA0165`). Extra fields RapidOCR computes (`state`, `confidence`, `box`, `raw_text`) are dropped by `PlateResult`.
- Docstrings in `orchestrator.py` and `pipeline/__init__.py` say "5-tier"/"Two-Stage"; the code is 4 tiers over 2 stages. Trust the code.
- Small files, one responsibility each; files mostly <100 lines. Prefer extending the existing module over adding layers.
- Commits: conventional (`fix:`, `test:`, `refactor:`, `feat:`); branches like `fix/<topic>`, `test/<topic>-<issue#>`; PRs into `main`.

## Testing

- `tests/test_*.py`, fixtures in `tests/conftest.py` (`client` = `TestClient(app)`, synthetic JPEG/PNG bytes; forces `ENABLE_MULTI_VEHICLE_OCR=False` per test).
- Real-image fixtures: `tests/images/1.jpg` … `57.jpg`.
- `tests/test_deploy.py` covers the deploy command templates; PR #28 adds guards that `run.sh` and the systemd unit never bind `0.0.0.0`.
- Coverage source is `app` (`uv run pytest --cov`).

## Deployment (summary — details in the spec)

`scripts/deploy.py` runs 4 SSH stages against the Pi: prep `/opt/argus` (+ ccache, uv) → `rsync --delete` repo incl. `yolo26n_openvino_model/` → `uv sync` + `nuitka --module --include-package=app` → move `app*.so` to `/opt/argus`, write `run.sh`, **delete all `.py` source** → install `argus.service` (`Restart=always`, `RestartSec=5`). CI (`.github/workflows/nuitka.yml`) builds the same `.so` on `ubuntu-26.04-arm` after green CI on `main` and force-pushes an orphan `release` branch.

## Where to look

| I want to… | Go to |
|---|---|
| Change a threshold / limit / port | `app/core/constants.py` (+ `app/services/detector/constants.py`) |
| Add an endpoint | `app/api/routes/` + register in `app/api/router.py` |
| Change response shape | `app/schemas.py` (`PlateResult`, `RecognitionResponse`) — breaking for Hermes/Janus, update the spec |
| Change tier order / fallback rules | `app/services/pipeline/orchestrator.py` |
| Fix a misread state code / char confusion | `app/services/plate_rules/corrections.py`, `char_maps.py` |
| Filter a new decal word | `app/services/plate_rules/decals.py` |
| Change deploy/systemd | `scripts/deploy_commands.py` + `tests/test_deploy.py` |
