"""Stage 2 OCR execution: per-vehicle crop scanning with Fast-ALPR and RapidOCR."""

from typing import Any

from app.core.config import settings
from app.core.exceptions import ANPRServiceError
from app.core.logging import logger
from app.schemas import DetectedVehicle, PlateResult
from app.services.pipeline.helpers import (
    _adjust_crop_coordinates,
    validate_plate_results,
)


def _ocr_single_vehicle(recognizer: Any, vehicle: DetectedVehicle, filename: str) -> list[PlateResult]:
    """Execute RapidOCR on a single vehicle crop with coordinate translation back to frame space."""
    if vehicle.crop is None:
        return []
    raw = recognizer.recognize(vehicle.crop, filename=filename)
    if any(r.get("plate") and r.get("plate") != "N/A" for r in raw):
        raw = _adjust_crop_coordinates(raw, vehicle.crop_box)
    return validate_plate_results(raw, vehicle_type=vehicle.vehicle_type, vehicle_box=vehicle.box)


def _scan_fast_alpr_crops(vehicles: list[DetectedVehicle]) -> list[PlateResult]:
    """Tier 1: Scan each vehicle in proximity order using Fast-ALPR."""
    from app.services.ocr.fast_alpr_runner import run_fast_alpr_on_vehicle

    results, seen = [], set()
    for v in vehicles:
        for p in run_fast_alpr_on_vehicle(v):
            if p.plate and p.plate != "N/A" and p.plate not in seen:
                seen.add(p.plate), results.append(p)
        if results and not settings.ENABLE_MULTI_VEHICLE_OCR:
            break
    return results


def _scan_rapidocr_crops(vehicles: list[DetectedVehicle], filename: str) -> list[PlateResult]:
    """Tier 3: Scan each vehicle in proximity order using RapidOCR."""
    import app.services.pipeline as pl

    recognizer, results, seen = pl.PlateRecognizer(), [], set()
    try:
        for v in vehicles:
            for p in _ocr_single_vehicle(recognizer, v, filename):
                if p.plate and p.plate != "N/A" and p.plate not in seen:
                    seen.add(p.plate), results.append(p)
            if results and not settings.ENABLE_MULTI_VEHICLE_OCR:
                break
    except (ANPRServiceError, ValueError, RuntimeError, OSError, KeyError, AttributeError) as exc:
        logger.error(f"OCR failed on '{filename}': {exc}")
        return []
    return results
