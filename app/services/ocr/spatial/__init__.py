"""2D spatial layout analysis, token pairing, and candidate selection package."""

from app.services.ocr.spatial.candidates import collect_candidates
from app.services.ocr.spatial.clustering import (
    cluster_horizontal_lines,
    compute_token_bounds,
    is_same_horizontal_line,
)
from app.services.ocr.spatial.enhancer import enhance_contrast, retry_contrast
from app.services.ocr.spatial.geometry import get_box_centroid, get_box_geometry
from app.services.ocr.spatial.pairing import build_spatial_pairs
from app.services.ocr.spatial.suppression import suppress_overlapping_candidates
from app.services.ocr.spatial.tokens import clean_and_filter_tokens

__all__ = [
    "build_spatial_pairs",
    "clean_and_filter_tokens",
    "cluster_horizontal_lines",
    "collect_candidates",
    "compute_token_bounds",
    "enhance_contrast",
    "get_box_centroid",
    "get_box_geometry",
    "is_same_horizontal_line",
    "retry_contrast",
    "suppress_overlapping_candidates",
]
