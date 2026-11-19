"""ANPR Pipeline Orchestrator: vehicle-first 5-tier cascaded fallback."""

import time
from typing import Any

from app.core.logging import logger
from app.schemas import PlateResult, RecognitionResponse
from app.services.image_processing import decode_image
from app.services.ocr.strategies import FastALPROCREngine, RapidOCREngine
from app.services.pipeline.helpers import _resolve_bytes
from app.services.pipeline.response import _build_response
from app.services.pipeline.sorting import sort_by_proximity


def _execute_cascade(prepared_img: Any, filename: str) -> list[PlateResult]:
    """Execute cascaded ANPR with vehicle detection and 4-tier fallbacks."""
    import app.services.pipeline as pl

    detection = pl.VehicleDetector().detect(prepared_img)
    vehicles = sort_by_proximity(detection.vehicles) if detection.vehicles else []
    logger.info(f"[pipeline] Stage 1: Detected {len(vehicles)} vehicle(s)")

    fast_alpr = FastALPROCREngine()
    results: list[PlateResult] = []
    if vehicles:
        logger.info(f"[pipeline] Tier 1: Scanning {len(vehicles)} vehicle crop(s) via Fast-ALPR")
        if results := fast_alpr.scan_crops(vehicles):
            logger.info(f"[pipeline] Tier 1 matched {len(results)} plate(s): {[r.plate for r in results]}")

    if not results:
        logger.info("[pipeline] Tier 2: Running Full-Frame Fast-ALPR fallback")
        if plates := fast_alpr.scan_full_frame(prepared_img):
            logger.info(f"[pipeline] Tier 2 matched {len(plates)} plate(s): {[r.plate for r in plates]}")
            return plates

    rapid_ocr = RapidOCREngine()
    if not results and vehicles:
        logger.info(f"[pipeline] Tier 3: Scanning {len(vehicles)} vehicle crop(s) via RapidOCR")
        if results := rapid_ocr.scan_crops(vehicles):
            logger.info(f"[pipeline] Tier 3 matched {len(results)} plate(s): {[r.plate for r in results]}")

    if not results:
        logger.info("[pipeline] Tier 4: Running Full-Frame RapidOCR fallback")
        return rapid_ocr.scan_full_frame(prepared_img, filename)
    return results


def recognize_plate_image(image_input: str | bytes, filename: str = "image.jpg") -> RecognitionResponse:
    """Process image through the 5-tier cascaded ANPR pipeline."""
    start_time, fn = time.time(), filename or (image_input if isinstance(image_input, str) else "image.jpg")
    logger.info(f"[pipeline] Starting ANPR for '{fn}'")
    plates = _execute_cascade(decode_image(_resolve_bytes(image_input)), fn)
    logger.info(f"[pipeline] Finished ANPR for '{fn}': {len(plates)} plate(s) found")
    return _build_response(plates, start_time)
