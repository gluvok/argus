# 01 - Repository Hygiene, Artifacts & Dependency Audit

## 1. Stray and Junk Artifacts Tracked in Git

Audit Command: `git ls-files | grep -E "(:memory:|\.onnx$|\.agents)"`

| Artifact | Size | Status | Problem & Risk |
|---|---|---|---|
| `:memory:.ses` | 51 B | Tracked in Git | Temporary session identifier committed to version control. Dead file. |
| `yolo26n.onnx` | 9.9 MB | Tracked in Git | Duplicate model weights. Argus uses `yolo26n_openvino_model/` for inference. This 10MB binary bloats git clone and is only copied conditionally in `.github/workflows/nuitka.yml:57`. |
| `.agents/skills/fastapi/*` | 7 files | Tracked in Git | Vendored external AI agent skills in repository root. |

## 2. Upstream Deprecations & Warnings

Audit Commands:
- `uv run pytest -W error::DeprecationWarning tests/test_fast_alpr_cascade.py`
- `uv run pytest -W error::starlette.exceptions.StarletteDeprecationWarning tests/test_api_recognition.py`

### Findings:
1. **Fast-ALPR `LicensePlateDetector` Deprecation**:
   - Location: `app/services/ocr/fast_alpr/engine.py:29`
   - Cause: Instantiating `ALPR(...)` without passing an explicit detector forwards to `DefaultDetector`, which calls the deprecated `LicensePlateDetector` instead of `create_detector` in `open_image_models.detection.factory`.
   - Fix: Use `create_detector("yolo-v9-s-608-license-plate-end2end", conf_thresh=0.25, providers=providers)` and inject `detector=...` into `ALPR()`.

2. **Starlette TestClient `StarletteDeprecationWarning`**:
   - Location: `starlette/testclient.py:47` invoked by `tests/conftest.py:45`
   - Cause: Starlette now recommends `httpx2` over `httpx` for testclient execution or configuring pytest filters for `StarletteDeprecationWarning`.

## 3. Formatting & Lint Baseline

Audit Command: `uv run ruff format --check .`
- **Result**: 62 files require formatting; 45 already formatted.
- `ruff check .` passed with 0 lint errors (`extend-select = ["T20", "FAST"]`).
