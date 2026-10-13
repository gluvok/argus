"""Fast-ALPR OCR strategy implementation."""

from app.schemas import DetectedVehicle, PlateResult
from app.services.image_processing import ImageInput
from app.services.ocr.fast_alpr_runner import (
    run_fast_alpr_on_vehicle,
    run_fast_alpr_pipeline,
)
from app.services.ocr.protocol import scan_crops_with_engine


class FastALPROCREngine:
    """Strategy wrapping Fast-ALPR execution on vehicle crops and full frames."""

    name: str = "Fast-ALPR"

    def scan_vehicle(self, vehicle: DetectedVehicle) -> list[PlateResult]:
        """Scan a single vehicle crop with Fast-ALPR."""
        return run_fast_alpr_on_vehicle(vehicle)

    def scan_crops(self, vehicles: list[DetectedVehicle]) -> list[PlateResult]:
        """Scan multiple vehicle crops in proximity order."""
        return scan_crops_with_engine(self, vehicles)

    def scan_full_frame(self, image: ImageInput, filename: str = "image.jpg") -> list[PlateResult]:
        """Execute full-frame Fast-ALPR fallback."""
        return run_fast_alpr_pipeline(image)
