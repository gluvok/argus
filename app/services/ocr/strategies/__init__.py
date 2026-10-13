"""OCR strategy implementations (Fast-ALPR and RapidOCR)."""

from app.services.ocr.strategies.fast_alpr import FastALPROCREngine
from app.services.ocr.strategies.rapidocr import RapidOCREngine

__all__ = ["FastALPROCREngine", "RapidOCREngine"]
