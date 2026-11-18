# 02 - Architectural Coupling & Circular Import Analysis

## 1. Circular Import Dependency Cycle

### Root Cause Analysis
A mutual dependency exists between `app.services.pipeline` and `app.services.ocr`:
1. `app.services.pipeline.__init__` imports `app.services.ocr.PlateRecognizer`.
2. `app.services.ocr.__init__` imports `app.services.ocr.strategies.RapidOCREngine`.
3. `RapidOCREngine` (in `app/services/ocr/strategies/rapidocr.py`) imports:
   - `_ocr_single_vehicle` from `app.services.pipeline.stages`
   - `run_full_frame_fallback` from `app.services.pipeline.fallback`
   - `PlateRecognizer` via `import app.services.pipeline as pl` inside `_rec()`
4. `app.services.pipeline.orchestrator` imports `FastALPROCREngine` and `RapidOCREngine` from `app.services.ocr.strategies`.
5. Because top-level imports of these modules cause an immediate circular `ImportError`, the codebase masked the cycle using function-level deferred imports:
   - `app/services/pipeline/orchestrator.py:17`: `import app.services.pipeline as pl` inside `_execute_cascade`
   - `app/services/ocr/strategies/rapidocr.py:25`: `import app.services.pipeline as pl` inside `_rec`
   - `app/services/ocr/recognizer.py:41`: `import app.services.ocr as ocr_mod` inside `parse_plate_info`

### Clean Architectural Solution:
- Move vehicle crop scanning and full-frame fallback orchestration to the `pipeline` package where orchestration belongs.
- `ocr` engines should strictly perform OCR text detection and recognition on an input image/crop and return tokens without importing pipeline stages.
- Once OCR engines do not import pipeline modules, all imports become unidirectional: `pipeline` -> `ocr` -> `core`.

---

## 2. Micro-File Fragmentation & Speculative Abstractions

### Inventory of Micro-Files:

| Directory | Files | Total Lines | Avg Lines/File | Identified Over-Engineering |
|---|---|---|---|---|
| `app/services/plate_rules` | 16 | 385 | 24 | Enterprise Specification Pattern (`PlateSpec` Protocol, `CompositePlateSpec`, `StatePrefixSpec`, `IndianPlateFormatSpec`, `DecalExclusionSpec`) spanning 6 files just to test regex & state code membership. |
| `app/services/ocr/spatial` | 8 | 267 | 33 | 8 files (`tokens.py`, `suppression.py`, `pairing.py`, `geometry.py`, `clustering.py`, `candidates.py`, `enhancer.py`, `__init__.py`) performing 2D bounding box sorting and grouping. |
| `app/services/pipeline` | 7 | 203 | 29 | `sorting.py` has 10 lines (a single 1-line function `sort_by_proximity`). `stages.py` is 19 lines. `response.py` is 19 lines. |

### Ponytail & Architecture Simplification Plan:
1. **Collapse `plate_rules`**:
   - Merge `specs/` (all 6 files) and `resolver.py` directly into a single cohesive `rules.py` module.
   - Replace the 5-class Specification hierarchy with a direct, single-function validator:
     ```python
     def is_valid_plate(plate: str) -> bool:
         return bool(INDIAN_PLATE_REGEX.fullmatch(plate) and plate[:2] in VALID_STATE_CODES)
     ```
   - Consolidate `char_maps.py`, `corrections.py`, `decals.py`, and `filters.py` into `constants.py` / `normalizers.py`.
2. **Consolidate `pipeline`**:
   - Merge 10-line `sorting.py`, 19-line `stages.py`, 19-line `response.py`, and 24-line `fallback.py` directly into `orchestrator.py` or a unified `stages.py`.
