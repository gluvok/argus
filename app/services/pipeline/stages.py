"""Stage 2 OCR execution: per-vehicle crop scanning with Fast-ALPR and RapidOCR."""

from typing import Any

from app.schemas import DetectedVehicle, PlateResult
from app.services.ocr.strategies import FastALPROCREngine, RapidOCREngine
from app.services.pipeline.helpers import (
    _adjust_crop_coordinates,
    validate_plate_results,
)


def _ocr_single_vehicle(recognizer: Any, vehicle: DetectedVehicle) -> list[PlateResult]:
    """Execute RapidOCR on a single vehicle crop with coordinate translation back to frame space."""
    if vehicle.crop is None:
        return []
    raw = recognizer.recognize(vehicle.crop)
    if any(r.get("plate") and r.get("plate") != "N/A" for r in raw):
        raw = _adjust_crop_coordinates(raw, vehicle.crop_box)
    return validate_plate_results(raw, vehicle_box=vehicle.box)


def _scan_fast_alpr_crops(vehicles: list[DetectedVehicle]) -> list[PlateResult]:
    """Tier 1: Scan each vehicle in proximity order using Fast-ALPR strategy."""
    return FastALPROCREngine().scan_crops(vehicles)


def _scan_rapidocr_crops(vehicles: list[DetectedVehicle], filename: str = "image.jpg") -> list[PlateResult]:
    """Tier 3: Scan each vehicle in proximity order using RapidOCR strategy."""
    return RapidOCREngine().scan_crops(vehicles)
