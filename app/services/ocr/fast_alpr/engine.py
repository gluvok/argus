"""Fast-ALPR Model Singleton and Warmup Engine."""

import threading
from typing import Any

from app.core.logging import logger
from app.services.image_processing import make_dummy_frame

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


def warm_up_fast_alpr() -> bool:
    """Pre-warm Fast-ALPR detector and OCR models with a synthetic crop."""
    try:
        engine = get_fast_alpr_engine()
        if engine is not None:
            engine.predict(make_dummy_frame(64, 128))
        return engine is not None
    except (RuntimeError, ValueError, OSError, AttributeError, ImportError) as exc:
        logger.error(f"Fast-ALPR warmup failed: {exc}")
        return False
