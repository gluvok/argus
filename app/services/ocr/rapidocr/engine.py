"""RapidOCR Model Singleton Engine."""

import logging
import threading

from rapidocr import RapidOCR

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
                from rapidocr import EngineType

                from app.core.constants import OPENVINO_NUM_THREADS

                params = {
                    "Det.engine_type": EngineType.OPENVINO,
                    "Cls.engine_type": EngineType.OPENVINO,
                    "Rec.engine_type": EngineType.OPENVINO,
                    "EngineConfig.openvino.inference_num_threads": OPENVINO_NUM_THREADS,
                }
                _rapidocr_instance = RapidOCR(params=params)
    return _rapidocr_instance

