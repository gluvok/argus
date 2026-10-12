"""ANPR Pipeline Orchestrator: vehicle-first 5-tier cascaded fallback."""

import time
from typing import Any

from app.core.config import settings
from app.schemas import DetectedVehicle, PlateResult, RecognitionResponse
from app.services.image_processing import decode_image
from app.services.ocr.fast_alpr_runner import run_fast_alpr_pipeline
from app.services.pipeline.fallback import _run_rapidocr_fullframe
from app.services.pipeline.helpers import _resolve_bytes
from app.services.pipeline.response import _build_response
from app.services.pipeline.stages import _scan_fast_alpr_crops, _scan_rapidocr_crops


def _sort_by_proximity(vehs: list[DetectedVehicle]) -> list[DetectedVehicle]:
    """Sort detected vehicles by proximity (closest first, largest box area)."""
    return sorted(vehs, key=lambda v: (v.box[2] - v.box[0]) * (v.box[3] - v.box[1]), reverse=True)


def _merge_plates(base: list[PlateResult], extra: list[PlateResult]) -> list[PlateResult]:
    """Merge and deduplicate plate results preserving order."""
    seen = {r.plate for r in base}
    return base + [r for r in extra if r.plate not in seen]


def _execute_cascade(prepared_img: Any, filename: str) -> list[PlateResult]:
    """Execute cascaded ANPR: vehicle detection -> crop Fast-ALPR -> FF Fast-ALPR -> crop RapidOCR -> FF RapidOCR."""
    import app.services.pipeline as pl

    detection = pl.VehicleDetector().detect(prepared_img)
    vehicles = _sort_by_proximity(detection.vehicles) if detection.vehicles else []
    results = _scan_fast_alpr_crops(vehicles) if vehicles else []

    if not results and (plates := run_fast_alpr_pipeline(prepared_img)):
        return plates

    if not results and vehicles:
        results = _scan_rapidocr_crops(vehicles, filename)

    if not results or settings.ENABLE_FULL_FRAME_OCR:
        ff = _run_rapidocr_fullframe(prepared_img, filename)
        results = _merge_plates(results, ff) if results else ff

    return results


def recognize_plate_image(image_input: str | bytes, filename: str = "image.jpg") -> RecognitionResponse:
    """Process image through the 5-tier cascaded ANPR pipeline."""
    start_time = time.time()
    resolved_fn = filename or (image_input if isinstance(image_input, str) else "image.jpg")
    prepared_img = decode_image(_resolve_bytes(image_input))
    plates = _execute_cascade(prepared_img, resolved_fn)
    return _build_response(plates, start_time)
