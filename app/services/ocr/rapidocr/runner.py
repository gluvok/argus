"""Execute RapidOCR inference and extract raw bounding tokens."""

from typing import Any

import numpy as np
from PIL import Image

from app.core.logging import logger
from app.schemas import OCRToken
from app.services.ocr.rapidocr.engine import get_rapidocr_engine
from app.services.ocr.spatial.geometry import get_box_geometry


def run_rapidocr_inference(img_pil: Image.Image, engine_getter: Any = None) -> list[OCRToken]:
    """Execute RapidOCR engine and return bounding tokens sorted vertically."""
    try:
        eng = engine_getter() if callable(engine_getter) else (engine_getter or get_rapidocr_engine())
        res = eng(np.array(img_pil))
        txts = getattr(res, "txts", None) if res else None
        scores = getattr(res, "scores", None) if res else None
        if not txts or not scores:
            return []
        boxes = getattr(res, "boxes", None)
        tokens: list[OCRToken] = []
        for idx, (t, s) in enumerate(zip(txts, scores, strict=False)):
            raw_b = boxes[idx] if (boxes is not None and idx < len(boxes)) else None
            cx, cy, bbox = get_box_geometry(raw_b)
            tokens.append(OCRToken(text=str(t), score=float(s), cx=cx, cy=cy, box=bbox))
        if any(item.cy is not None for item in tokens):
            tokens.sort(key=lambda x: x.cy if x.cy is not None else 9999.0)
        return tokens
    except (RuntimeError, ValueError, TypeError, IndexError, AttributeError, OSError) as e:
        logger.error(f"[ocr/rapidocr] OCR execution failed: {e}")
        return []
