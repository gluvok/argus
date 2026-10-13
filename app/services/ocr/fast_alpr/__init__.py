"""Fast-ALPR engine and execution runner package."""

from app.services.ocr.fast_alpr.engine import (
    check_fast_alpr_engine,
    get_fast_alpr_engine,
)
from app.services.ocr.fast_alpr.padding import compute_padded_crop
from app.services.ocr.fast_alpr.runner import (
    run_fast_alpr,
    run_fast_alpr_on_vehicle,
    run_fast_alpr_pipeline,
)

__all__ = [
    "check_fast_alpr_engine",
    "compute_padded_crop",
    "get_fast_alpr_engine",
    "run_fast_alpr",
    "run_fast_alpr_on_vehicle",
    "run_fast_alpr_pipeline",
]
