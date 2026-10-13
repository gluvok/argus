"""Vehicle spatial proximity sorting."""

from app.schemas import DetectedVehicle
from app.services.detector.box import BoundingBox


def sort_by_proximity(vehs: list[DetectedVehicle]) -> list[DetectedVehicle]:
    """Sort detected vehicles by proximity (closest first, largest box area)."""
    return sorted(vehs, key=lambda v: BoundingBox(*v.box).area, reverse=True)

