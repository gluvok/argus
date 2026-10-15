"""Bounding box coordinate validation, clamping, and containment math."""

from typing import Any

from app.core.contracts import require
from app.services.detector.box import BoundingBox
from app.services.detector.constants import MIN_CROP_EDGE_PX


def clamp_box(box: Any, width: int, height: int) -> BoundingBox | None:
    """Clamp an (x1, y1, x2, y2) bounding box to valid image pixel coordinates."""
    require(width > 0 and height > 0, f"dimensions must be positive, got {width}x{height}")
    if not box or not isinstance(box, (tuple, list)) or len(box) != 4:
        return None
    try:
        x1, y1, x2, y2 = (int(v) for v in box)
    except (TypeError, ValueError):
        return None

    if x2 < x1:
        x1, x2 = x2, x1
    if y2 < y1:
        y1, y2 = y2, y1

    x1, y1, x2, y2 = max(0, min(x1, width)), max(0, min(y1, height)), max(0, min(x2, width)), max(0, min(y2, height))

    if x2 - x1 < MIN_CROP_EDGE_PX or y2 - y1 < MIN_CROP_EDGE_PX:
        return None
    return BoundingBox(x1, y1, x2, y2)



def is_contained(inner: tuple[int, int, int, int], outer: tuple[int, int, int, int], threshold: float = 0.80) -> bool:
    """Check if inner box is predominantly contained within outer box."""
    return BoundingBox(*outer).contains(inner, threshold)


def box_iou(a: tuple[int, int, int, int], b: tuple[int, int, int, int]) -> float:
    """Compute Intersection-over-Union (IoU) between two bounding boxes."""
    return BoundingBox(*a).iou(b)


__all__ = ["BoundingBox", "box_iou", "clamp_box", "is_contained"]


