"""Concrete Strategy implementations for OCR engines (Fast-ALPR and RapidOCR)."""

from typing import Any

from app.core.exceptions import ANPRServiceError
from app.core.logging import logger
from app.schemas import DetectedVehicle, PlateResult
from app.services.image_processing import ImageInput
from app.services.ocr.fast_alpr_runner import (
    run_fast_alpr_on_vehicle,
    run_fast_alpr_pipeline,
)
from app.services.ocr.protocol import scan_crops_with_engine

_OCR_ERRORS = (ANPRServiceError, ValueError, RuntimeError, OSError, KeyError, AttributeError)


class FastALPROCREngine:
    """Strategy wrapping Fast-ALPR execution."""

    name: str = "Fast-ALPR"

    def scan_vehicle(self, vehicle: DetectedVehicle) -> list[PlateResult]:
        return run_fast_alpr_on_vehicle(vehicle)

    def scan_crops(self, vehicles: list[DetectedVehicle]) -> list[PlateResult]:
        return scan_crops_with_engine(self, vehicles)

    def scan_full_frame(self, image: ImageInput, filename: str = "image.jpg") -> list[PlateResult]:
        return run_fast_alpr_pipeline(image)


class RapidOCREngine:
    """Strategy wrapping RapidOCR execution."""

    name: str = "RapidOCR"

    def __init__(self, recognizer: Any = None) -> None:
        self.recognizer = recognizer

    def _rec(self) -> Any:
        if self.recognizer is not None:
            return self.recognizer
        import app.services.pipeline as pl
        return pl.PlateRecognizer()

    def scan_vehicle(self, vehicle: DetectedVehicle) -> list[PlateResult]:
        from app.services.pipeline.stages import _ocr_single_vehicle
        try:
            return _ocr_single_vehicle(self._rec(), vehicle)
        except _OCR_ERRORS as exc:
            logger.error(f"RapidOCR crop scan failed: {exc}")
            return []

    def scan_crops(self, vehicles: list[DetectedVehicle]) -> list[PlateResult]:
        return scan_crops_with_engine(self, vehicles)

    def scan_full_frame(self, image: ImageInput, filename: str = "image.jpg") -> list[PlateResult]:
        from app.services.pipeline.fallback import run_full_frame_fallback
        return run_full_frame_fallback(self._rec(), image, filename)
