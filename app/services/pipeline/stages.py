"""Single-vehicle crop OCR coordinate translation and plate validation."""

from typing import Any

from app.schemas import DetectedVehicle, PlateResult
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
