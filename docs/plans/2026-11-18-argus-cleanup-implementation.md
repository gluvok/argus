# Argus System Remediation & Agile Cleanup Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Remediate all architectural circular dependencies, upload DoS vectors, concurrency race hazards, micro-file sprawl, and upstream deprecations in Argus with zero version conflicts, rigorous TDD, and full ECC verification.

**Architecture:** Unidirectional layered pipeline: decouple OCR and pipeline boundaries, enforce streaming upload size validation before RAM buffering, guard AI singletons with thread locks, collapse single-use Specification micro-files, and gate all changes through the 6-phase ECC Verification Loop.

**Tech Stack:** Python 3.14, FastAPI, Ultralytics YOLO26 OpenVINO, Fast-ALPR ONNX, RapidOCR OpenVINO, Pytest, Ruff, Ty, Uv.

---

### Skills Assignment Matrix

| Task | Primary Skills | Role in Task |
|---|---|---|
| **Task 1: Repo Hygiene** | `@clean-code`, `@ponytail` | Prune dead tracked session files and duplicate 10MB weights |
| **Task 2: Upload DoS Guard** | `@fastapi-pro`, `@find-bugs`, `@security-audit`, `@test-driven-development` | Stream chunked upload validation to prevent memory exhaustion |
| **Task 3: CORS & Pixel Budget** | `@security-audit`, `@api-security-testing`, `@test-driven-development` | Strict CORS policy and startup pixel budget initialization |
| **Task 4: Concurrency Lock** | `@systematic-debugging`, `@performance-profiling`, `@test-driven-development` | Thread-safe double-checked locking on YOLO model singleton |
| **Task 5: Fast-ALPR Deprecation** | `@systematic-debugging`, `@test-driven-development`, `@clean-code` | Migrate to modern `create_detector` API and eliminate warnings |
| **Task 6: Circular Import Decoupling** | `@architecture`, `@systematic-debugging`, `@clean-code` | Decouple OCR strategies and pipeline orchestration |
| **Task 7: Micro-File Consolidation** | `@ponytail`, `@clean-code`, `@architecture` | Collapse 6-file Specification pattern and 1-line modules |
| **Task 8: Benchmark Sanitization** | `@benchmark`, `@performance-profiling`, `@clean-code` | Make benchmark read-only and eliminate test image mutation |
| **Task 9: ECC Verification Audit** | `@verification-loop`, `@find-bugs`, `@code-review-checklist`, `@kaizen` | Execute complete 6-phase quality gate before completion |

---

### Task 1: Repository Hygiene & Git Cleanup

**Skills:** `@clean-code`, `@ponytail`

**Files:**
- Untrack: `:memory:.ses`
- Untrack: `yolo26n.onnx`
- Modify: `.gitignore`
- Modify: `.github/workflows/nuitka.yml:56-58`

**Step 1: Write the verification test**
Run a check for tracked artifacts:
```bash
cd /Users/kaalu/importante/argus && git ls-files | grep -E "(:memory:|\.onnx$)"
```
Expected: Outputs `:memory:.ses` and `yolo26n.onnx`.

**Step 2: Untrack artifacts from Git index**
```bash
cd /Users/kaalu/importante/argus && git rm --cached :memory:.ses yolo26n.onnx
```
Expected: `rm ':memory:.ses'`, `rm 'yolo26n.onnx'`.

**Step 3: Update `.gitignore` and `.github/workflows/nuitka.yml`**
Add to `.gitignore`:
```gitignore
# Temporary session dumps
:memory:.ses
*.ses

# Standalone ONNX weights (Active engine uses yolo26n_openvino_model/)
yolo26n.onnx
```
In `.github/workflows/nuitka.yml`, delete line 57:
```yaml
- [ -f yolo26n.onnx ] && cp yolo26n.onnx "${RELEASE_DIR}/"
```

**Step 4: Verify test passes**
```bash
cd /Users/kaalu/importante/argus && git ls-files | grep -E "(:memory:|\.onnx$)" || echo "CLEAN"
```
Expected: `CLEAN`.

**Step 5: Commit**
```bash
cd /Users/kaalu/importante/argus && git add .gitignore .github/workflows/nuitka.yml
git commit -m "chore: remove untracked session dump and redundant onnx weights from git"
```

---

### Task 2: Security Hardening — Streaming Chunked Upload Guard (TDD)

**Skills:** `@fastapi-pro`, `@find-bugs`, `@security-audit`, `@test-driven-development`

**Files:**
- Create: `tests/test_upload_limits.py`
- Modify: `app/services/image_processing/security.py`
- Modify: `app/api/routes/recognition.py`

**Step 1: Write the failing tests**
Add to `tests/test_upload_limits.py`:
```python
import io
import pytest
from app.core.exceptions import PayloadTooLargeError
from app.services.image_processing.security import read_upload_stream


@pytest.mark.anyio
async def test_read_upload_stream_rejects_oversized_chunked():
    """Verify stream reading halts and raises PayloadTooLargeError without buffering full payload."""

    class MockStream:
        def __init__(self, size_bytes: int):
            self.remaining = size_bytes
            self.chunk_size = 64 * 1024

        async def read(self, size: int = -1) -> bytes:
            if self.remaining <= 0:
                return b""
            to_read = min(self.chunk_size, self.remaining)
            self.remaining -= to_read
            return b"X" * to_read

    # 8MB + 128KB payload stream
    stream = MockStream(8 * 1024 * 1024 + 128 * 1024)
    with pytest.raises(
        PayloadTooLargeError, match="Image exceeds maximum permitted size"
    ):
        await read_upload_stream(stream, max_bytes=8 * 1024 * 1024)


@pytest.mark.anyio
async def test_read_upload_stream_accepts_valid_payload():
    """Verify stream reading succeeds within permitted size limit."""

    class ValidStream:
        def __init__(self, data: bytes):
            self.buf = io.BytesIO(data)

        async def read(self, size: int = -1) -> bytes:
            return self.buf.read(size)

    payload = b"TEST_IMAGE_BYTES"
    result = await read_upload_stream(ValidStream(payload), max_bytes=1024)
    assert result == payload
```

**Step 2: Run test to verify it fails**
```bash
cd /Users/kaalu/importante/argus && uv run pytest tests/test_upload_limits.py::test_read_upload_stream_rejects_oversized_chunked
```
Expected: FAIL (`ImportError: cannot import name 'read_upload_stream'`).

**Step 3: Write minimal implementation**
In `app/services/image_processing/security.py`:
```python
async def read_upload_stream(file: Any, max_bytes: int = MAX_UPLOAD_BYTES) -> bytes:
    """Read upload file in chunks, raising PayloadTooLargeError immediately if cap is exceeded."""
    chunk_size = 64 * 1024
    buffer = bytearray()
    while chunk := await file.read(chunk_size):
        buffer.extend(chunk)
        if len(buffer) > max_bytes:
            limit_mb = max_bytes // (1024 * 1024)
            raise PayloadTooLargeError(
                f"Image exceeds maximum permitted size of {limit_mb} MB."
            )
    return bytes(buffer)
```
In `app/api/routes/recognition.py`:
```python
from app.services.image_processing.security import (
    read_upload_stream,
    validate_image_upload,
)


@router.post("/recognize", summary="Recognize Vehicle License Plate")
async def recognize_plate(
    file: Annotated[UploadFile, File(description="Image file (JPEG, PNG, WebP, BMP)")],
    semaphore: InferenceSemaphore,
) -> RecognitionResponse:
    """Process an uploaded vehicle image through the 4-Tier Cascaded ANPR Pipeline."""
    image_bytes = await read_upload_stream(file)
    validate_image_upload(image_bytes, content_type=file.content_type)
    async with semaphore:
        return await asyncify(recognize_plate_image)(
            image_bytes,
            filename=file.filename or "image.jpg",
        )
```

**Step 4: Run test to verify it passes**
```bash
cd /Users/kaalu/importante/argus && uv run pytest tests/test_upload_limits.py
```
Expected: PASS.

**Step 5: Commit**
```bash
cd /Users/kaalu/importante/argus && git add app/api/routes/recognition.py app/services/image_processing/security.py tests/test_upload_limits.py
git commit -m "fix(security): implement chunked upload streaming bounds to eliminate memory exhaustion DoS"
```

---

### Task 3: Security & Config Hardening — Strict CORS & Pixel Budget Init (TDD)

**Skills:** `@security-audit`, `@api-security-testing`, `@test-driven-development`

**Files:**
- Modify: `tests/test_core.py`
- Modify: `app/core/constants.py`

**Step 1: Write the failing tests**
Add to `tests/test_core.py`:
```python
import subprocess
import sys
from PIL import Image
from app.core import constants


def test_cors_credentials_not_allowed_with_wildcard():
    """Verify that wildcard CORS does not enable credentials."""
    if "*" in constants.CORS_ORIGINS:
        assert constants.CORS_ALLOW_CREDENTIALS is False, (
            "CORS allow_credentials must be False when allow_origins is wildcard '*'"
        )


def test_pil_max_image_pixels_set_at_constants_import():
    """Verify Image.MAX_IMAGE_PIXELS is configured without needing loader.py imported."""
    code = "from PIL import Image; import app.core.constants as c; assert Image.MAX_IMAGE_PIXELS == c.MAX_IMAGE_PIXELS"
    result = subprocess.run([sys.executable, "-c", code], capture_output=True)
    assert result.returncode == 0, result.stderr.decode()
```

**Step 2: Run test to verify it fails**
```bash
cd /Users/kaalu/importante/argus && uv run pytest tests/test_core.py::test_cors_credentials_not_allowed_with_wildcard
```
Expected: FAIL (`AssertionError: CORS allow_credentials must be False when allow_origins is wildcard '*'`).

**Step 3: Write minimal implementation**
In `app/core/constants.py`:
```python
from PIL import Image

# ...
CORS_ORIGINS: list[str] = ["*"]
CORS_ALLOW_CREDENTIALS = False
# ...
MAX_IMAGE_PIXELS = 50_000_000
Image.MAX_IMAGE_PIXELS = MAX_IMAGE_PIXELS
```

**Step 4: Run test to verify it passes**
```bash
cd /Users/kaalu/importante/argus && uv run pytest tests/test_core.py
```
Expected: PASS.

**Step 5: Commit**
```bash
cd /Users/kaalu/importante/argus && git add app/core/constants.py tests/test_core.py
git commit -m "fix(security): disallow credentials on wildcard CORS and enforce PIL pixel budget on startup"
```

---

### Task 4: Concurrency Hardening — Thread-Safe VehicleDetector Singleton (TDD)

**Skills:** `@systematic-debugging`, `@performance-profiling`, `@test-driven-development`

**Files:**
- Modify: `tests/test_services.py`
- Modify: `app/services/detector/detector.py`

**Step 1: Write the failing test**
Add to `tests/test_services.py`:
```python
import threading
from app.services.detector import VehicleDetector


def test_vehicle_detector_thread_safe_singleton():
    """Verify VehicleDetector acquires a thread lock and returns consistent singleton."""
    assert hasattr(VehicleDetector, "_lock")
    assert isinstance(VehicleDetector._lock, type(threading.Lock()))

    instances = []

    def get_inst():
        instances.append(VehicleDetector.get_model())

    threads = [threading.Thread(target=get_inst) for _ in range(10)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert all(inst is instances[0] for inst in instances)
```

**Step 2: Run test to verify it fails**
```bash
cd /Users/kaalu/importante/argus && uv run pytest tests/test_services.py::test_vehicle_detector_thread_safe_singleton
```
Expected: FAIL (`AssertionError: assert hasattr(VehicleDetector, '_lock')`).

**Step 3: Write minimal implementation**
In `app/services/detector/detector.py`:
```python
import threading


class VehicleDetector:
    """Stage 1: YOLO26 Vehicle Detection."""

    _model: YOLO | None = None
    _lock = threading.Lock()
    _clamp_box = staticmethod(clamp_box)
    _parse_detections = staticmethod(parse_detections)

    @classmethod
    def get_model(cls) -> YOLO:
        if cls._model is None:
            with cls._lock:
                if cls._model is None:
                    import app.services.detector as yf

                    cls._model = yf.YOLO(constants.YOLO_MODEL_NAME)
        ensure(cls._model is not None, "YOLO model failed to initialise")
        return cls._model
```

**Step 4: Run test to verify it passes**
```bash
cd /Users/kaalu/importante/argus && uv run pytest tests/test_services.py::test_vehicle_detector_thread_safe_singleton
```
Expected: PASS.

**Step 5: Commit**
```bash
cd /Users/kaalu/importante/argus && git add app/services/detector/detector.py tests/test_services.py
git commit -m "fix(concurrency): add double-checked thread lock to VehicleDetector singleton"
```

---

### Task 5: Upstream Deprecation Remediation — Fast-ALPR create_detector (TDD)

**Skills:** `@systematic-debugging`, `@test-driven-development`, `@clean-code`

**Files:**
- Modify: `tests/test_fast_alpr_cascade.py`
- Modify: `app/services/ocr/fast_alpr/engine.py`

**Step 1: Verify the failing warning condition**
```bash
cd /Users/kaalu/importante/argus && uv run pytest -W error::DeprecationWarning tests/test_fast_alpr_cascade.py::test_fast_alpr_blank_frame_no_coreml_error
```
Expected: FAIL (`DeprecationWarning: LicensePlateDetector is deprecated; use create_detector instead.`).

**Step 2: Write minimal implementation**
In `app/services/ocr/fast_alpr/engine.py`:
```python
from open_image_models import create_detector
from fast_alpr import ALPR


def get_fast_alpr_engine() -> Any:
    """Return thread-safe singleton instance of Fast-ALPR engine using modern create_detector API."""
    global _alpr_instance
    if _alpr_instance is None:
        with _lock:
            if _alpr_instance is None:
                logger.info("Initializing Fast-ALPR ONNX models...")
                providers = _resolve_onnx_providers()
                detector = create_detector(
                    "yolo-v9-s-608-license-plate-end2end",
                    conf_thresh=0.25,
                    providers=providers,
                )
                _alpr_instance = ALPR(
                    detector=detector,
                    ocr_model="cct-xs-v2-global-model",
                    ocr_providers=providers,
                )
    return _alpr_instance
```

**Step 3: Run test with `-W error::DeprecationWarning` to verify it passes**
```bash
cd /Users/kaalu/importante/argus && uv run pytest -W error::DeprecationWarning tests/test_fast_alpr_cascade.py::test_fast_alpr_blank_frame_no_coreml_error
```
Expected: PASS with 0 warnings.

**Step 4: Commit**
```bash
cd /Users/kaalu/importante/argus && git add app/services/ocr/fast_alpr/engine.py
git commit -m "refactor(ocr): migrate Fast-ALPR to create_detector API to eliminate LicensePlateDetector deprecation"
```

---

### Task 6: Architectural Decoupling — Eliminate Pipeline/OCR Circular Imports

**Skills:** `@architecture`, `@systematic-debugging`, `@clean-code`

**Files:**
- Modify: `tests/test_ocr_strategies.py`
- Modify: `app/services/ocr/strategies/rapidocr.py`
- Modify: `app/services/pipeline/orchestrator.py`

**Step 1: Write the architectural decoupling test**
Add to `tests/test_ocr_strategies.py`:
```python
import subprocess
import sys


def test_ocr_module_isolated_from_pipeline():
    """Verify app.services.ocr does not import pipeline package."""
    code = (
        "import sys; "
        "import app.services.ocr.strategies; "
        "assert 'app.services.pipeline' not in sys.modules, "
        "'app.services.ocr.strategies illegally imported app.services.pipeline'"
    )
    result = subprocess.run([sys.executable, "-c", code], capture_output=True)
    assert result.returncode == 0, result.stderr.decode()
```

**Step 2: Run test to verify it fails**
```bash
cd /Users/kaalu/importante/argus && uv run pytest tests/test_ocr_strategies.py::test_ocr_module_isolated_from_pipeline
```
Expected: FAIL (`AssertionError: app.services.ocr.strategies illegally imported app.services.pipeline`).

**Step 3: Write minimal implementation**
In `app/services/ocr/strategies/rapidocr.py`:
- Remove `import app.services.pipeline as pl` inside `_rec()`. Instead import `PlateRecognizer` directly from `app.services.ocr.recognizer`.
- In `scan_vehicle` and `scan_full_frame`: delegate inference directly to `self._rec().recognize()` rather than calling `app.services.pipeline.stages._ocr_single_vehicle`.

In `app/services/pipeline/orchestrator.py`:
- Move `from app.services.detector import VehicleDetector` to top-level.
- Remove `import app.services.pipeline as pl` from inside `_execute_cascade()`.

**Step 4: Run test to verify it passes**
```bash
cd /Users/kaalu/importante/argus && uv run pytest tests/test_ocr_strategies.py tests/test_pipeline.py
```
Expected: PASS.

**Step 5: Commit**
```bash
cd /Users/kaalu/importante/argus && git add app/services/ocr/strategies/rapidocr.py app/services/pipeline/orchestrator.py tests/test_ocr_strategies.py
git commit -m "refactor(architecture): decouple pipeline and ocr packages to eliminate circular dependencies"
```

---

### Task 7: Ponytail Codebase Simplification — Consolidate Micro-Files

**Skills:** `@ponytail`, `@clean-code`, `@architecture`, `@code-review-checklist`

**Files:**
- Remove: `app/services/pipeline/sorting.py`
- Consolidate into: `app/services/pipeline/helpers.py`
- Remove: `app/services/plate_rules/specs/composite.py`
- Remove: `app/services/plate_rules/specs/decal.py`
- Remove: `app/services/plate_rules/specs/format.py`
- Remove: `app/services/plate_rules/specs/protocol.py`
- Remove: `app/services/plate_rules/specs/state_prefix.py`
- Consolidate into: `app/services/plate_rules/specs/__init__.py`
- Test: `tests/test_plate_specs.py`, `tests/test_pipeline.py`

**Step 1: Verify current baseline**
```bash
cd /Users/kaalu/importante/argus && uv run pytest tests/test_plate_specs.py tests/test_pipeline.py
```
Expected: PASS.

**Step 2: Consolidate `sort_by_proximity` into `app/services/pipeline/helpers.py`**
Move function into `helpers.py`:
```python
def sort_by_proximity(vehs: list[DetectedVehicle]) -> list[DetectedVehicle]:
    """Sort detected vehicles by proximity (closest first, largest box area)."""
    return sorted(vehs, key=lambda v: BoundingBox(*v.box).area, reverse=True)
```
Update imports in `orchestrator.py` and `app/services/pipeline/__init__.py`. Remove `sorting.py`.

**Step 3: Consolidate `plate_rules/specs/` into `specs/__init__.py`**
Combine `PlateSpec`, `NonDecalSpec`, `StatePrefixSpec`, `IndianPlateFormatSpec`, `CompositePlateSpec`, and `STANDARD_PLATE_SPEC` into `app/services/plate_rules/specs/__init__.py` (~45 lines).
Delete the 5 redundant micro-files (`composite.py`, `decal.py`, `format.py`, `protocol.py`, `state_prefix.py`).

**Step 4: Run tests to verify zero regressions**
```bash
cd /Users/kaalu/importante/argus && uv run pytest tests/test_plate_specs.py tests/test_pipeline.py
```
Expected: PASS.

**Step 5: Commit**
```bash
cd /Users/kaalu/importante/argus && git rm app/services/pipeline/sorting.py app/services/plate_rules/specs/composite.py app/services/plate_rules/specs/decal.py app/services/plate_rules/specs/format.py app/services/plate_rules/specs/protocol.py app/services/plate_rules/specs/state_prefix.py
git add app/services/pipeline/ app/services/plate_rules/
git commit -m "refactor(ponytail): collapse 1-function sorting module and consolidate specification micro-files"
```

---

### Task 8: Tooling Hygiene & Benchmark Sanitization

**Skills:** `@benchmark`, `@performance-profiling`, `@clean-code`

**Files:**
- Move: `test_direct.py` -> `scripts/benchmark.py`
- Modify: `scripts/benchmark.py`
- Modify: `pyproject.toml`
- Test: `tests/test_benchmark_script.py`

**Step 1: Write test verifying read-only execution**
Create `tests/test_benchmark_script.py`:
```python
import os
from scripts.benchmark import natural_key


def test_benchmark_natural_key_sorting():
    files = ["10.jpg", "1.jpg", "2.jpg", "20.jpg"]
    sorted_files = sorted(files, key=natural_key)
    assert sorted_files == ["1.jpg", "2.jpg", "10.jpg", "20.jpg"]
```

**Step 2: Relocate and make benchmark read-only**
```bash
cd /Users/kaalu/importante/argus && git mv test_direct.py scripts/benchmark.py
```
In `scripts/benchmark.py`:
- Remove `serialize_images()` in-place disk renaming loop. Replace with read-only natural sorting.
- Set default `REPORT_FILE = "docs/analysis/benchmark_report.md"`.

In `pyproject.toml`:
```toml
[tool.ruff.lint.per-file-ignores]
"tests/*" = ["T201"]
"scripts/benchmark.py" = ["T201"]
```

**Step 3: Run test to verify**
```bash
cd /Users/kaalu/importante/argus && uv run pytest tests/test_benchmark_script.py
```
Expected: PASS.

**Step 4: Commit**
```bash
cd /Users/kaalu/importante/argus && git add scripts/benchmark.py pyproject.toml tests/test_benchmark_script.py
git commit -m "chore(tooling): relocate benchmark to scripts/ and make execution strictly read-only"
```

---

### Task 9: Formatting & ECC 6-Phase Verification Audit Loop

**Skills:** `@verification-loop`, `@find-bugs`, `@code-review-checklist`, `@kaizen`

**Files:**
- Format: Entire repository

**Step 1: Format entire codebase via Ruff**
```bash
cd /Users/kaalu/importante/argus && uv run ruff format .
```
Expected: Formats all files to 100% compliance.

**Step 2: Phase 1 — Build & Lockfile Verification**
```bash
cd /Users/kaalu/importante/argus && uv lock --check
```
Expected: `Resolved 126 packages in ...ms` (Zero version conflicts).

**Step 3: Phase 2 — Type Check Verification**
```bash
cd /Users/kaalu/importante/argus && uv run ty check app scripts tests
```
Expected: `All checks passed!`.

**Step 4: Phase 3 — Lint Check Verification**
```bash
cd /Users/kaalu/importante/argus && uv run ruff check . && uv run ruff format --check .
```
Expected: `All checks passed! All files already formatted`.

**Step 5: Phase 4 — Test Suite & Coverage Verification**
```bash
cd /Users/kaalu/importante/argus && uv run pytest --cov=app --cov-report=term-missing
```
Expected: `185+ passed, 0 failures, 0 errors, ≥99% coverage`.

**Step 6: Phase 5 — Security Scan**
Scan for credentials or private keys:
```bash
cd /Users/kaalu/importante/argus && grep -rn "sk-" --exclude-dir={.venv,.git} . || true
```
Expected: Zero secrets discovered.

**Step 7: Phase 6 — Diff Review**
```bash
cd /Users/kaalu/importante/argus && git diff --stat HEAD~8
```
Expected: Clean, disciplined diff verifying all 8 tasks without extraneous edits.

**Step 8: Commit final verification gate**
```bash
cd /Users/kaalu/importante/argus && git add -A && git commit -m "chore: complete 6-phase ECC verification audit"
```
