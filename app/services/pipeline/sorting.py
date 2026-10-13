"""Vehicle spatial proximity sorting."""

from app.schemas import DetectedVehicle


def sort_by_proximity(vehs: list[DetectedVehicle]) -> list[DetectedVehicle]:
    """Sort detected vehicles by proximity (closest first, largest box area)."""
    return sorted(vehs, key=lambda v: (v.box[2] - v.box[0]) * (v.box[3] - v.box[1]), reverse=True)

