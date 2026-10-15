"""Stage 1: YOLO26 Vehicle Detection and Cropper."""

from ultralytics import YOLO

from app.services.detector.detector import VehicleDetector
from app.services.detector.geometry import (
    BoundingBox,
    box_iou,
    clamp_box,
    is_contained,
)

__all__ = [
    "YOLO",
    "BoundingBox",
    "VehicleDetector",
    "box_iou",
    "clamp_box",
    "is_contained",
]


