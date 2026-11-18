# Argus Deep Analysis & Cleanup Readiness Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Execute a systematic deep analysis of the Argus ANPR microservice to identify architectural, security, concurrency, code hygiene, and test debt, synthesizing findings into an actionable Agile cleanup backlog.

**Architecture:** Multi-phase diagnostic framework using systematic debugging and code inspection to audit module boundaries, eliminate circular dependencies, evaluate attack surfaces, stress-test inference concurrency, and establish an iterative Lean Kanban cleanup backlog.

**Tech Stack:** Python 3.14, FastAPI, Ultralytics YOLO26 OpenVINO, Fast-ALPR ONNX, RapidOCR OpenVINO, Pytest, Ruff, Uv.

---

### Relevant Skills Mapping

| Skill | Purpose in Analysis & Cleanup |
|---|---|
| `@architecture` | Audit system boundaries, evaluate trade-offs, decouple circular dependencies, formulate ADRs |
| `@systematic-debugging` | Root-cause analysis of deprecation warnings, thread-safety hazards, and runtime errors |
| `@ponytail` | Enforce radical simplicity: eliminate single-use abstractions, prune dead code, collapse micro-files |
| `@no-ai-slop` | Ensure reports, ADRs, and documentation are concise, concrete, and free of fluff |
| `@find-bugs` | Map attack surface for DoS vectors, memory exhaustion on uploads, and insecure CORS headers |
| `@security-audit` | Audit REST endpoints, payload boundaries, and deployment script execution paths |
| `@fastapi-pro` | Audit asynchronous threadpool delegation (`asyncer`), lifecycle hooks, and streaming validation |
| `@clean-code` | Eliminate duplication, standardize naming, and align module cohesion |
| `@code-review-checklist` | Systematic verification of functionality, error handling, performance, and maintainability |
| `@performance-profiling` | Benchmark latency, memory profile AI engine cascades, and evaluate Pi 5 hardware targets |
| `@kaizen` | Standardize continuous improvement loops and define actionable Agile cleanup milestones |

---

### Agile Framework for Post-Analysis Cleanup

To transition smoothly from Deep Analysis to Code Cleanup, Argus will employ **Lean Kanban with Iterative Milestones**:

1. **Phase 1: Discovery & Spike (This Plan)** — Deep analysis across all system dimensions. Outputs a prioritized Product Backlog.
2. **Phase 2: Backlog Triage & Estimation** — Categorize findings into 3 focused iterations:
   - **Sprint 1 (Hygiene & Decoupling)**: Delete repo artifacts (`:memory:.ses`, redundant weights), break circular imports, merge micro-files.
   - **Sprint 2 (Security & Concurrency)**: Chunked upload streaming, strict CORS, thread-safe YOLO singleton.
   - **Sprint 3 (Tooling & Deprecations)**: Modernize Fast-ALPR and Starlette testclient APIs, format codebase via Ruff, relocate benchmarks.
3. **WIP Limits & Definition of Done (DoD)**:
   - Max 2 tasks in progress concurrently.
   - Every cleanup task must pass: 100% of existing 184 tests, 0 Ruff lint/format errors, no regression in mean latency (≤50ms on Tier 1).

---

### Task 1: Repository Hygiene, Artifacts & Dependency Audit

**Files:**
- Audit: `/Users/kaalu/importante/argus/:memory:.ses`
- Audit: `/Users/kaalu/importante/argus/yolo26n.onnx`
- Audit: `/Users/kaalu/importante/argus/pyproject.toml`
- Audit: `/Users/kaalu/importante/argus/uv.lock`
- Audit: `/Users/kaalu/importante/argus/skills-lock.json`
- Target Report: `/Users/kaalu/importante/argus/docs/analysis/01-repo-hygiene-audit.md`

**Step 1: Check untracked and junk files tracked in Git**
- Inspect `:memory:.ses` (session dump committed to git).
- Verify redundancy of `yolo26n.onnx` (9.9 MB ONNX weight file committed to git while `yolo26n_openvino_model/` is the active engine).
- Audit `.agents/skills/fastapi/` (7 vendored markdown files).

Run:
```bash
cd /Users/kaalu/importante/argus && git ls-files | grep -E "(:memory:|\.onnx$|\.agents)"
```
Expected output: Lists `:memory:.ses`, `yolo26n.onnx`, and `.agents/skills/fastapi/*`.

**Step 2: Audit Python 3.14 runtime compatibility & dependency deprecations**
- Check for deprecation warnings in test suite:
  - `StarletteDeprecationWarning: Using httpx with starlette.testclient is deprecated`
  - `DeprecationWarning: LicensePlateDetector is deprecated; use create_detector instead`

Run:
```bash
cd /Users/kaalu/importante/argus && uv run pytest -W error::DeprecationWarning tests/test_fast_alpr_cascade.py
```
Expected output: Identification of exact line where `LicensePlateDetector` is invoked.

**Step 3: Audit Ruff formatting baseline**
- Check formatting status across all 107 files.

Run:
```bash
cd /Users/kaalu/importante/argus && uv run ruff format --check .
```
Expected output: Lists 62 unformatted files.

**Step 4: Save findings to report**
Write verified issues into `docs/analysis/01-repo-hygiene-audit.md`.

---

### Task 2: Architectural Coupling & Circular Import Analysis

**Files:**
- Inspect: `app/services/pipeline/orchestrator.py:15-45`
- Inspect: `app/services/ocr/strategies/rapidocr.py:22-47`
- Inspect: `app/services/ocr/recognizer.py:40-45`
- Inspect: `app/services/plate_rules/specs/` (all 5 micro-files)
- Inspect: `app/services/pipeline/sorting.py`
- Target Report: `/Users/kaalu/importante/argus/docs/analysis/02-architecture-coupling-audit.md`

**Step 1: Trace hidden circular dependencies**
- Investigate why `import app.services.pipeline as pl` is deferred inside `_execute_cascade` in `app/services/pipeline/orchestrator.py`.
- Investigate why `import app.services.pipeline as pl` is deferred inside `_rec()` in `app/services/ocr/strategies/rapidocr.py`.
- Trace dependency chain: `pipeline.orchestrator` -> `ocr.strategies` -> `pipeline.stages` / `pipeline.fallback` -> `pipeline.orchestrator`.

Run:
```bash
cd /Users/kaalu/importante/argus && uv run python -c "from app.services.ocr.strategies import RapidOCREngine; from app.services.pipeline.orchestrator import _execute_cascade; print('Imported successfully')"
```
Expected output: Check if top-level imports create circular `ImportError`.

**Step 2: Audit micro-file fragmentation against Ponytail & Architecture standards**
- Audit `app/services/plate_rules/`: 16 files for 385 lines of code (avg 24 lines/file).
  - Analyze `CompositePlateSpec`, `PlateSpec` protocol, `StatePrefixSpec`, `IndianPlateFormatSpec`: evaluate if Specification pattern adds unnecessary abstraction over direct regex validation.
- Audit `app/services/pipeline/sorting.py`: 10 lines containing a single 1-line function.
- Audit `app/services/ocr/spatial/`: 8 files for 267 lines of code.

Run:
```bash
wc -l /Users/kaalu/importante/argus/app/services/plate_rules/specs/*.py
```
Expected output: Detailed breakdown showing each file is ≤ 18 lines.

**Step 3: Document consolidation architecture**
Propose domain-aligned module boundaries that collapse micro-files, eliminate cyclic dependencies, and allow clean top-level imports.

---

### Task 3: Security & Input Boundary Attack Surface Audit

**Files:**
- Inspect: `app/api/routes/recognition.py:16-28`
- Inspect: `app/services/image_processing/security.py:15-51`
- Inspect: `app/core/constants.py:16-20`
- Inspect: `app/core/middleware.py:13-21`
- Inspect: `scripts/deploy_commands.py:13-34`
- Target Report: `/Users/kaalu/importante/argus/docs/analysis/03-security-attack-surface-audit.md`

**Step 1: Audit multipart upload memory exhaustion (DoS vector)**
- Analyze `app/api/routes/recognition.py`: `image_bytes = await file.read()` loads the entire uploaded file into RAM before `validate_image_upload` checks `MAX_UPLOAD_BYTES` (8 MB).
- Formulate hypothesis: An attacker streaming a 2GB file can trigger an Out-Of-Memory (OOM) kill on a Raspberry Pi 5.

Run:
```bash
cd /Users/kaalu/importante/argus && uv run python -c "
from app.services.image_processing.security import probe_image
from app.core.exceptions import PayloadTooLargeError
try:
    probe_image(b'0' * (9 * 1024 * 1024))
except PayloadTooLargeError:
    print('Guard works on bytes, but endpoint reads all bytes before guard')
"
```
Expected output: Confirmation of validation timing mismatch.

**Step 2: Audit CORS policy violation**
- Check `app/core/constants.py`: `CORS_ORIGINS = ["*"]` combined with `CORS_ALLOW_CREDENTIALS = True`.
- Per W3C CORS specification and OWASP guidelines, `Access-Control-Allow-Origin: *` with credentials is fundamentally invalid in browsers and rejected by modern clients.

**Step 3: Audit deployment script shell execution**
- Check `scripts/deploy_commands.py`: `curl -LsSf https://astral.sh/uv/install.sh | sh` executed without checksum verification over SSH.

**Step 4: Save findings to report**
Write vulnerability analysis and suggested fixes into `docs/analysis/03-security-attack-surface-audit.md`.

---

### Task 4: Concurrency & Engine Lifecycle Diagnostics

**Files:**
- Inspect: `app/services/detector/detector.py:22-30`
- Inspect: `app/services/ocr/rapidocr/engine.py:17-35`
- Inspect: `app/services/ocr/fast_alpr/engine.py:19-37`
- Inspect: `app/core/lifespan.py:14-26`
- Inspect: `app/api/dependencies.py:1-25`
- Target Report: `/Users/kaalu/importante/argus/docs/analysis/04-concurrency-lifecycle-audit.md`

**Step 1: Audit singleton thread-safety under concurrent load**
- Notice `RapidOCR` and `Fast-ALPR` use `threading.Lock()` when initializing instances.
- Contrast with `VehicleDetector.get_model()` in `app/services/detector/detector.py`:
  ```python
  if cls._model is None:
      cls._model = yf.YOLO(...)
  ```
  No lock is acquired! Under concurrent requests on startup, multiple threads can race to initialize `cls._model`.
- Analyze inference concurrency: `app/api/dependencies.py` permits up to 4 concurrent inferences via `InferenceSemaphore(4)`. Verify whether OpenVINO compiled models or YOLO inference methods tolerate concurrent calls without thread-local contexts or locks.

Run:
```bash
cd /Users/kaalu/importante/argus && uv run python -c "
import threading
from app.services.detector.detector import VehicleDetector
print('Checking VehicleDetector lock presence:', hasattr(VehicleDetector, '_lock'))
"
```
Expected output: `Checking VehicleDetector lock presence: False`.

**Step 2: Profile startup lifespan blocking**
- Evaluate `app/core/lifespan.py`: `VehicleDetector.warm_up()` and `warm_up_ocr()` execute synchronously on the main thread during FastAPI startup.
- Measure exact startup latency.

Run:
```bash
cd /Users/kaalu/importante/argus && uv run python -c "
import time
start = time.perf_counter()
from app.services.detector import VehicleDetector
from app.services.ocr import warm_up_ocr
VehicleDetector.warm_up()
warm_up_ocr()
print(f'Lifespan warmup duration: {(time.perf_counter() - start)*1000:.2f} ms')
"
```
Expected output: Warmup duration logged in ms.

---

### Task 5: Test Suite Hygiene & Benchmark Tooling Audit

**Files:**
- Inspect: `test_direct.py:40-65`
- Inspect: `tests/test_enhancements_v2.py`
- Inspect: `tests/test_indian_anpr_enhancements.py`
- Inspect: `tests/test_hardening.py`
- Inspect: `tests/images/`
- Target Report: `/Users/kaalu/importante/argus/docs/analysis/05-test-suite-hygiene-audit.md`

**Step 1: Audit test file organization and redundant tests**
- Check test naming: `test_enhancements_v2.py`, `test_indian_anpr_enhancements.py`, and `test_hardening.py` represent temporal patch test files rather than domain-aligned structure (`test_detector.py`, `test_ocr.py`, `test_rules.py`).
- Inspect test overlap and coverage gaps across the 184 tests.

**Step 2: Audit `test_direct.py` side-effects**
- `test_direct.py:40-65`: Notice `serialize_images` actively renames files on disk in `tests/images/` to `1.jpg`..`N.jpg`.
- Notice `test_direct.py:154`: Directly writes `benchmark_report.md` in the project root directory.
- Evaluate moving `test_direct.py` to `scripts/benchmark.py` and making it strictly read-only with a configurable output directory.

Run:
```bash
head -n 60 /Users/kaalu/importante/argus/test_direct.py | grep -E "(rename|open\(REPORT_FILE|staging)"
```
Expected output: Verifies disk mutation code in root benchmark script.

---

### Task 6: Synthesis & Agile Backlog Formulation

**Files:**
- Create: `/Users/kaalu/importante/argus/docs/analysis/SUMMARY.md`
- Create: `/Users/kaalu/importante/argus/docs/backlog/CLEANUP_BACKLOG.md`

**Step 1: Consolidate findings from Tasks 1–5 into an Executive Audit Summary**
- Aggregate all identified debt:
  1. Repo Hygiene: Stray `:memory:.ses`, redundant 10MB `yolo26n.onnx`, 62 unformatted files.
  2. Architecture: Circular imports masked by lazy function imports, over-abstracted Specification pattern (16 files for 385 lines), 10-line micro-files.
  3. Security: Unbounded `file.read()` upload DoS vector, invalid `CORS_ALLOW_CREDENTIALS` + wildcard origin.
  4. Concurrency: Lock-free `VehicleDetector.get_model()` race condition.
  5. Tooling: In-place file mutation in `test_direct.py`, Starlette / Fast-ALPR deprecation warnings.

**Step 2: Construct the Lean Kanban Cleanup Backlog**
Organize cleanup cards into 3 Sprint Iterations with explicit priority, effort estimate (Story Points), files touched, and Definition of Done:
- **Sprint 1 (Architecture & Hygiene)**:
  - Card 1.1: Untrack `:memory:.ses` and clean git history / `.gitignore`.
  - Card 1.2: Remove redundant `yolo26n.onnx` from git tracking and clean `.github/workflows/nuitka.yml`.
  - Card 1.3: Break circular dependencies between `pipeline` and `ocr.strategies`.
  - Card 1.4: Collapse `app/services/plate_rules` micro-files (merge `specs/` into domain rules, collapse 10-line modules).
  - Card 1.5: Format codebase with `ruff format .`.
- **Sprint 2 (Security & Concurrency Hardening)**:
  - Card 2.1: Implement chunked streaming upload size limit in `app/api/routes/recognition.py`.
  - Card 2.2: Fix CORS configuration in `app/core/constants.py` and `app/core/middleware.py`.
  - Card 2.3: Add thread-safety lock to `VehicleDetector.get_model()`.
- **Sprint 3 (Testing, Tooling & Modernization)**:
  - Card 3.1: Relocate `test_direct.py` to `scripts/benchmark.py` and remove disk mutation logic.
  - Card 3.2: Update Fast-ALPR API to resolve `LicensePlateDetector` deprecation warning.
  - Card 3.3: Reorganize patch tests (`test_enhancements_v2`, `test_hardening`) into clean domain modules.

**Step 3: Verify plan and backlog completeness**
Run full test suite to confirm baseline remains 100% green before cleanup begins:
```bash
cd /Users/kaalu/importante/argus && uv run pytest
```
Expected output: `184 passed in ~20s`.
