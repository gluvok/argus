"""Input resolution, coordinate translation, and output validation helpers."""

from typing import Any

from pydantic import ValidationError

from app.core.exceptions import InvalidImageError
from app.schemas import PlateResult


def validate_plate_results(
    raw_results: Any,
    vehicle_box: tuple[int, int, int, int] | None = None,
) -> list[PlateResult]:
    """Validate and convert raw dictionary outputs into PlateResult Pydantic schemas."""
    if not isinstance(raw_results, list):
        return []
    validated: list[PlateResult] = []
    for item in raw_results:
        if isinstance(item, dict) and item.get("plate") and item.get("plate") != "N/A":
            entry = dict(item)
            if vehicle_box is not None:
                entry.setdefault("vehicle_box", vehicle_box)
            try:
                validated.append(PlateResult.model_validate(entry))
            except ValidationError:
                continue
    return validated


def _resolve_bytes(image_input: str | bytes) -> bytes:
    """Read polymorphic image input into raw in-memory bytes."""
    if isinstance(image_input, bytes):
        return image_input
    if isinstance(image_input, str):
        try:
            return open(image_input, "rb").read()
        except Exception as e:
            raise InvalidImageError(f"Failed to read image file '{image_input}': {e}") from e
    raise InvalidImageError(f"Unsupported image input type: {type(image_input).__name__}")


def _adjust_crop_coordinates(raw: list[dict[str, Any]], crop_box: tuple[int, int, int, int] | None) -> list[dict[str, Any]]:
    """Translate plate bounding box coordinates from crop space to full image frame space."""
    if not crop_box:
        return raw
    cx1, cy1 = crop_box[0], crop_box[1]
    adjusted: list[dict[str, Any]] = []
    for item in raw:
        entry = dict(item)
        if (b := entry.get("box")) and isinstance(b, (tuple, list)) and len(b) >= 4:
            entry["box"] = (int(b[0] + cx1), int(b[1] + cy1), int(b[2] + cx1), int(b[3] + cy1))
        adjusted.append(entry)
    return adjusted

