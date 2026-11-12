"""Fast-ALPR engine and execution runner package."""

from app.services.ocr.fast_alpr.engine import (
    get_fast_alpr_engine,
    warm_up_fast_alpr,
)
from app.services.ocr.fast_alpr.padding import compute_padded_crop
from app.services.ocr.fast_alpr.runner import (
    run_fast_alpr,
    run_fast_alpr_on_vehicle,
    run_fast_alpr_pipeline,
)

__all__ = [
    "compute_padded_crop",
    "get_fast_alpr_engine",
    "run_fast_alpr",
    "run_fast_alpr_on_vehicle",
    "run_fast_alpr_pipeline",
    "warm_up_fast_alpr",
]
