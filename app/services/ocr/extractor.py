"""Extract license plates from image using OCR tokens, spatial lines, and candidates."""

from typing import Any

from PIL import Image

from app.services.ocr.rapidocr import run_rapidocr_inference
from app.services.ocr.spatial import (
    build_spatial_pairs,
    clean_and_filter_tokens,
    cluster_horizontal_lines,
    collect_candidates,
    suppress_overlapping_candidates,
)


def extract_plates(img_pil: Image.Image, engine_getter: Any, parse_fn: Any) -> list[dict[str, Any]]:
    """Extract and validate Indian license plates from a PIL image array."""
    raw_items = run_rapidocr_inference(img_pil, engine_getter)
    if not raw_items:
        return []
    clean_tokens, raw_summary = clean_and_filter_tokens(raw_items)
    lines = cluster_horizontal_lines(clean_tokens)
    pairs = build_spatial_pairs(clean_tokens)
    candidates = collect_candidates(clean_tokens, lines, pairs, raw_summary, parse_fn)
    if candidates:
        candidates.sort(key=lambda c: (round(c.confidence, 2), len(c.info.get("plate", "")), -c.rank, c.y_pos), reverse=True)
        suppressed = suppress_overlapping_candidates(candidates)
        if suppressed:
            return [c.info for c in suppressed]
    return [{"plate": "N/A", "state": "N/A", "raw_text": raw_summary, "confidence": None, "box": None}]

