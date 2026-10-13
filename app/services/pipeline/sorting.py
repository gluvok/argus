"""Vehicle spatial proximity sorting and plate result deduplication."""

from app.schemas import DetectedVehicle, PlateResult


def sort_by_proximity(vehs: list[DetectedVehicle]) -> list[DetectedVehicle]:
    """Sort detected vehicles by proximity (closest first, largest box area)."""
    return sorted(vehs, key=lambda v: (v.box[2] - v.box[0]) * (v.box[3] - v.box[1]), reverse=True)


def merge_plates(base: list[PlateResult], extra: list[PlateResult]) -> list[PlateResult]:
    """Merge and deduplicate plate results preserving order."""
    seen = {r.plate for r in base}
    return base + [r for r in extra if r.plate not in seen]
