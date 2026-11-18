"""
Argus: Production Indian Automatic Number Plate Recognition (ANPR) Python Library & Service.
"""

from typing import Any

from app.schemas import (
    DetectedVehicle,
    PlateResult,
    RecognitionResponse,
)

__all__ = [
    "DetectedVehicle",
    "PlateResult",
    "RecognitionResponse",
    "recognize_plate_image",
]


def __getattr__(name: str) -> Any:
    if name == "recognize_plate_image":
        from app.services.pipeline.orchestrator import recognize_plate_image

        return recognize_plate_image
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
