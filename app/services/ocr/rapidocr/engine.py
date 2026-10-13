"""RapidOCR Model Singleton and Warmup Engine."""

import logging
import threading

from rapidocr import RapidOCR

from app.core.logging import logger

_rapid_logger = logging.getLogger("RapidOCR")
_rapid_logger.setLevel(logging.ERROR)
for _h in _rapid_logger.handlers:
    _h.setLevel(logging.ERROR)

_rapidocr_instance: RapidOCR | None = None
_lock = threading.Lock()


def get_rapidocr_engine() -> RapidOCR:
    """Return thread-safe singleton instance of RapidOCR engine."""
    global _rapidocr_instance
    if _rapidocr_instance is None:
        with _lock:
            if _rapidocr_instance is None:
                from app.core.constants import ONNX_NUM_THREADS

                params = {"EngineConfig.onnxruntime.intra_op_num_threads": ONNX_NUM_THREADS}
                _rapidocr_instance = RapidOCR(params=params)
    return _rapidocr_instance


def check_rapidocr_engine() -> bool:
    """Pre-warm and verify RapidOCR models during lifespan startup."""
    try:
        return get_rapidocr_engine() is not None
    except (RuntimeError, ValueError, OSError, AttributeError, ImportError) as exc:
        logger.error(f"RapidOCR warmup failed: {exc}")
        return False
