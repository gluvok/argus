"""Full-frame fallback routine for RapidOCR."""

from typing import Any

from app.core.exceptions import ANPRServiceError
from app.core.logging import logger
from app.schemas import PlateResult
from app.services.image_processing import ImageInput
from app.services.pipeline.helpers import validate_plate_results


def run_full_frame_fallback(
    recognizer: Any,
    image_input: ImageInput,
    filename: str,
) -> list[PlateResult]:
    """Execute full-frame RapidOCR when vehicle crops yield no plates or no vehicles detected."""
    logger.info(f"Running full-frame RapidOCR fallback on '{filename}'")
    try:
        raw = recognizer.recognize(image_input)
        return validate_plate_results(raw)
    except (ANPRServiceError, ValueError, RuntimeError, OSError, KeyError, AttributeError) as exc:
        logger.error(f"Full-frame OCR failed on '{filename}': {exc}")
        return []
