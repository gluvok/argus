"""Fast-ALPR Model Singleton Engine."""

import threading
from typing import Any

from app.core.logging import logger

_alpr_instance: Any = None
_lock = threading.Lock()


def _resolve_onnx_providers() -> list[str]:
    """Return available ONNX execution providers excluding CoreML."""
    import onnxruntime as ort

    return [p for p in ort.get_available_providers() if p != "CoreMLExecutionProvider"]


def get_fast_alpr_engine() -> Any:
    """Return thread-safe singleton instance of Fast-ALPR engine."""
    global _alpr_instance
    if _alpr_instance is None:
        with _lock:
            if _alpr_instance is None:
                from fast_alpr import ALPR

                logger.info("Initializing Fast-ALPR ONNX models...")
                providers = _resolve_onnx_providers()
                _alpr_instance = ALPR(
                    detector_model="yolo-v9-s-608-license-plate-end2end",
                    detector_conf_thresh=0.25,
                    detector_providers=providers,
                    ocr_model="cct-xs-v2-global-model",
                    ocr_providers=providers,
                )
    return _alpr_instance

