"""OCREngine Strategy Protocol for uniform OCR inference execution."""

from typing import Any, Protocol, runtime_checkable

from app.core.config import settings
from app.schemas import DetectedVehicle, PlateResult
from app.services.image_processing import ImageInput


@runtime_checkable
class OCREngine(Protocol):
    """Uniform Strategy Protocol for OCR inference engines."""

    @property
    def name(self) -> str:
        """Human-readable name of the OCR engine."""
        ...

    def scan_vehicle(self, vehicle: DetectedVehicle) -> list[PlateResult]:
        """Scan a single vehicle crop and return extracted plate results."""
        ...

    def scan_crops(self, vehicles: list[DetectedVehicle]) -> list[PlateResult]:
        """Scan vehicle crops in proximity order."""
        ...

    def scan_full_frame(self, image: ImageInput, filename: str = "image.jpg") -> list[PlateResult]:
        """Fallback scan on full camera frame."""
        ...


def scan_crops_with_engine(engine: Any, vehicles: list[DetectedVehicle]) -> list[PlateResult]:
    """Scan vehicle crops in proximity order using the provided engine."""
    results, seen = [], set()
    for v in vehicles:
        for p in engine.scan_vehicle(v):
            if p.plate and p.plate != "N/A" and p.plate not in seen:
                seen.add(p.plate), results.append(p)
        if results and not settings.ENABLE_MULTI_VEHICLE_OCR:
            break
    return results
