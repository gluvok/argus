"""Stage 2: License Plate Text Recognition (OCR) and Spatial Candidate Selection."""

from typing import Any

from PIL import Image

from app.core.contracts import require
from app.schemas import OCRToken, PlateCandidate
from app.services.image_processing import ImageInput, load_rgb
from app.services.ocr.extractor import extract_plates
from app.services.ocr.rapidocr import (
    check_rapidocr_engine,
    get_rapidocr_engine,
    run_rapidocr_inference,
)
from app.services.ocr.spatial import (
    build_spatial_pairs,
    clean_and_filter_tokens,
    cluster_horizontal_lines,
    collect_candidates,
    compute_token_bounds,
    enhance_contrast,
    get_box_centroid,
    get_box_geometry,
    is_same_horizontal_line,
    retry_contrast,
)


class PlateRecognizer:
    """ANPR Engine using RapidOCR ONNX Runtime with 2D spatial layout candidate pairing."""

    get_rapidocr_engine = staticmethod(get_rapidocr_engine)
    check_rapidocr_engine = staticmethod(check_rapidocr_engine)
    _enhance_contrast = staticmethod(enhance_contrast)
    _get_box_geometry = staticmethod(get_box_geometry)
    _get_box_centroid = staticmethod(get_box_centroid)
    _is_same_horizontal_line = staticmethod(is_same_horizontal_line)
    _cluster_horizontal_lines = staticmethod(cluster_horizontal_lines)
    _build_spatial_pairs = staticmethod(build_spatial_pairs)
    _compute_token_bounds = staticmethod(compute_token_bounds)
    _clean_and_filter_tokens = staticmethod(clean_and_filter_tokens)

    @staticmethod
    def parse_plate_info(raw_plate: str | None) -> dict[str, Any] | None:
        import app.services.ocr as ocr_mod

        return ocr_mod.parse_plate_info(raw_plate)

    def _run_ocr_inference(self, img: Image.Image) -> list[OCRToken]:
        return run_rapidocr_inference(img, self.get_rapidocr_engine)

    def _collect_candidates(self, toks: list[OCRToken], l: list[list[OCRToken]], p: list[Any], s: str) -> list[PlateCandidate]:
        return collect_candidates(toks, l, p, s, self.parse_plate_info)

    def _extract_plates_from_image_array(self, img: Image.Image) -> list[dict[str, Any]]:
        return extract_plates(img, self.get_rapidocr_engine, self.parse_plate_info)

    def recognize(self, image_input: ImageInput) -> list[dict[str, Any]]:
        require(image_input is not None, "recognize() called with no image")
        img = load_rgb(image_input)
        res = self._extract_plates_from_image_array(img)
        if any(r.get("plate") and r.get("plate") != "N/A" for r in res):
            return res
        return retry_contrast(self, img) or res
