"""Unified OCR Model Pre-warming for Fast-ALPR and RapidOCR."""

from collections.abc import Callable
from typing import Any

from app.core.logging import logger
from app.services.image_processing import make_dummy_frame
from app.services.ocr.fast_alpr import get_fast_alpr_engine
from app.services.ocr.rapidocr import get_rapidocr_engine

_WARMUP_ERRORS = (RuntimeError, ValueError, OSError, AttributeError, ImportError)


def _warm_up_engine(name: str, getter: Callable[[], Any], run_pass: Callable[[Any], None]) -> bool:
    """Warm up a single OCR engine with a synthetic dummy frame."""
    try:
        engine = getter()
        if engine is not None:
            run_pass(engine)
        return engine is not None
    except _WARMUP_ERRORS as exc:
        logger.error(f"{name} warmup failed: {exc}")
        return False


def warm_up_ocr() -> bool:
    """Pre-warm both Fast-ALPR and RapidOCR engines on synthetic dummy crops."""
    dummy = make_dummy_frame(64, 128)
    fast_ok = _warm_up_engine("Fast-ALPR", get_fast_alpr_engine, lambda eng: eng.predict(dummy))
    rapid_ok = _warm_up_engine("RapidOCR", get_rapidocr_engine, lambda eng: eng(dummy))
    return fast_ok and rapid_ok

