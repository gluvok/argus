"""Tests for the 5-tier cascaded vehicle-first ANPR fallback pipeline."""

from unittest.mock import MagicMock, patch

import numpy as np
from PIL import Image

from app.schemas import DetectedVehicle, DetectionResult, PlateResult
from app.services.ocr.fast_alpr_padding import compute_padded_crop
from app.services.pipeline.orchestrator import recognize_plate_image


def test_fast_alpr_padding_expansion():
    """Verify compute_padded_crop correctly applies 15% X and 10% Y margin expansion."""
    dummy_img = np.zeros((100, 100, 3), dtype=np.uint8)
    bbox = MagicMock(x1=20, y1=20, x2=60, y2=40)
    crop = compute_padded_crop(dummy_img, bbox, pad_x_pct=0.15, pad_y_pct=0.10)
    assert crop.shape[0] == 30
    assert crop.shape[1] == 60


@patch("app.services.pipeline.orchestrator.run_fast_alpr_pipeline")
@patch("app.services.pipeline.orchestrator._scan_fast_alpr_crops")
@patch("app.services.pipeline.VehicleDetector.detect")
def test_cascade_tier1_crop_fast_alpr_early_exit(
    mock_yolo, mock_fast_crop, mock_fast_ff, sample_image_bytes
):
    """Tier 1: Vehicle detected and crop Fast-ALPR finds plate; full-frame is skipped."""
    mock_yolo.return_value = DetectionResult(
        vehicles=[DetectedVehicle(vehicle_type="car", box=(10, 10, 50, 50), crop=Image.new("RGB", (40, 40)))]
    )
    mock_fast_crop.return_value = [PlateResult(plate="RJ09GA0165", vehicle_box=(10, 10, 50, 50))]

    resp = recognize_plate_image(sample_image_bytes, filename="clear_plate.jpg")

    assert mock_yolo.call_count == 1
    assert mock_fast_crop.call_count == 1
    assert mock_fast_ff.call_count == 0
    assert len(resp.results) == 1
    assert resp.results[0].plate == "RJ09GA0165"
    assert resp.results[0].vehicle_box == (10, 10, 50, 50)
    assert resp.results[0].execution_time_ms > 0


from app.core.config import settings


@patch("app.services.ocr.fast_alpr_runner.run_fast_alpr")
@patch("app.services.pipeline.VehicleDetector.detect")
def test_cascade_tier1_multi_vehicle_closest_order_strict_plates(
    mock_yolo, mock_run_fast_alpr, sample_image_bytes
):
    """Tier 1: 3 vehicles (v1 unplated, v2 plated, v3 plated) returns exactly 2 results."""
    dummy_crop = Image.new("RGB", (40, 40))
    # v1: 100x100 (area 10000 - closest), v2: 80x80 (area 6400), v3: 50x50 (area 2500)
    v1 = DetectedVehicle(vehicle_type="car", box=(0, 0, 100, 100), crop=dummy_crop)
    v2 = DetectedVehicle(vehicle_type="truck", box=(0, 0, 80, 80), crop=dummy_crop)
    v3 = DetectedVehicle(vehicle_type="bus", box=(0, 0, 50, 50), crop=dummy_crop)
    mock_yolo.return_value = DetectionResult(vehicles=[v3, v1, v2])

    # Side effect for v1 (closest), v2 (second closest), v3 (third closest)
    mock_run_fast_alpr.side_effect = [
        [],  # v1 crop: unplated
        ["DL01AB1234"],  # v2 crop: plated
        ["HR26CD5678"],  # v3 crop: plated
    ]

    with patch.object(settings, "ENABLE_MULTI_VEHICLE_OCR", True):
        resp = recognize_plate_image(sample_image_bytes, filename="three_vehicles.jpg")

    assert len(resp.results) == 2
    assert resp.results[0].plate == "DL01AB1234"
    assert resp.results[0].vehicle_box == (0, 0, 80, 80)
    assert resp.results[1].plate == "HR26CD5678"
    assert resp.results[1].vehicle_box == (0, 0, 50, 50)


@patch("app.services.pipeline.orchestrator.run_fast_alpr_pipeline")
@patch("app.services.pipeline.orchestrator._scan_fast_alpr_crops")
@patch("app.services.pipeline.VehicleDetector.detect")
def test_cascade_tier2_crop_miss_full_frame_fast_alpr(
    mock_yolo, mock_fast_crop, mock_fast_ff, sample_image_bytes
):
    """Tier 2: Crop Fast-ALPR misses, full-frame Fast-ALPR succeeds."""
    mock_yolo.return_value = DetectionResult(
        vehicles=[DetectedVehicle(vehicle_type="car", box=(10, 10, 50, 50), crop=Image.new("RGB", (40, 40)))]
    )
    mock_fast_crop.return_value = []
    mock_fast_ff.return_value = [PlateResult(plate="MH12AB1234", vehicle_box=None)]

    resp = recognize_plate_image(sample_image_bytes, filename="distant_vehicle.jpg")

    assert mock_fast_crop.call_count == 1
    assert mock_fast_ff.call_count == 1
    assert len(resp.results) == 1
    assert resp.results[0].plate == "MH12AB1234"
    assert resp.results[0].vehicle_box is None


@patch("app.services.pipeline.orchestrator.run_fast_alpr_pipeline")
@patch("app.services.pipeline.VehicleDetector.detect")
def test_cascade_tier2_tractor_zero_vehicle_fast_alpr(
    mock_yolo, mock_fast_ff, sample_image_bytes
):
    """Tier 2: Zero vehicles detected (tractor/non-COCO) falls back to full-frame Fast-ALPR."""
    mock_yolo.return_value = DetectionResult(vehicles=[])
    mock_fast_ff.return_value = [PlateResult(plate="PB08EE1234", vehicle_box=None)]

    resp = recognize_plate_image(sample_image_bytes, filename="tractor.jpg")

    assert mock_fast_ff.call_count == 1
    assert len(resp.results) == 1
    assert resp.results[0].plate == "PB08EE1234"
    assert resp.results[0].vehicle_box is None


@patch("app.services.pipeline.orchestrator._run_rapidocr_fullframe")
@patch("app.services.pipeline.orchestrator._scan_rapidocr_crops")
@patch("app.services.pipeline.orchestrator.run_fast_alpr_pipeline")
@patch("app.services.pipeline.orchestrator._scan_fast_alpr_crops")
@patch("app.services.pipeline.VehicleDetector.detect")
def test_cascade_tier3_crop_rapidocr_fallback(
    mock_yolo, mock_fast_crop, mock_fast_ff, mock_rapid_crop, mock_rapid_ff, sample_image_bytes
):
    """Tier 3: Fast-ALPR fails on crop and full frame; crop RapidOCR succeeds with vehicle_box."""
    mock_yolo.return_value = DetectionResult(
        vehicles=[DetectedVehicle(vehicle_type="truck", box=(10, 10, 50, 50), crop=Image.new("RGB", (40, 40)))]
    )
    mock_fast_crop.return_value = []
    mock_fast_ff.return_value = []
    mock_rapid_crop.return_value = [PlateResult(plate="UP14AB9999", vehicle_box=(10, 10, 50, 50))]

    resp = recognize_plate_image(sample_image_bytes, filename="dirty_plate.jpg")

    assert mock_fast_crop.call_count == 1
    assert mock_fast_ff.call_count == 1
    assert mock_rapid_crop.call_count == 1
    assert mock_rapid_ff.call_count == 0
    assert len(resp.results) == 1
    assert resp.results[0].plate == "UP14AB9999"
    assert resp.results[0].vehicle_box == (10, 10, 50, 50)


@patch("app.services.pipeline.orchestrator._run_rapidocr_fullframe")
@patch("app.services.pipeline.orchestrator._scan_rapidocr_crops")
@patch("app.services.pipeline.orchestrator.run_fast_alpr_pipeline")
@patch("app.services.pipeline.orchestrator._scan_fast_alpr_crops")
@patch("app.services.pipeline.VehicleDetector.detect")
def test_cascade_tier4_full_frame_rapidocr_fallback(
    mock_yolo, mock_fast_crop, mock_fast_ff, mock_rapid_crop, mock_rapid_ff, sample_image_bytes
):
    """Tier 4: All crop passes and full-frame Fast-ALPR fail; full-frame RapidOCR succeeds."""
    mock_yolo.return_value = DetectionResult(vehicles=[])
    mock_fast_ff.return_value = []
    mock_rapid_ff.return_value = [PlateResult(plate="DL01XY9999", vehicle_box=None)]

    resp = recognize_plate_image(sample_image_bytes, filename="full_fallback.jpg")

    assert mock_fast_ff.call_count == 1
    assert mock_rapid_ff.call_count == 1
    assert len(resp.results) == 1
    assert resp.results[0].plate == "DL01XY9999"
    assert resp.results[0].vehicle_box is None


@patch("app.services.pipeline.orchestrator._run_rapidocr_fullframe")
@patch("app.services.pipeline.orchestrator.run_fast_alpr_pipeline")
@patch("app.services.pipeline.VehicleDetector.detect")
def test_cascade_all_tiers_empty_returns_clean_response(
    mock_yolo, mock_fast_ff, mock_rapid_ff, sample_image_bytes
):
    """When all tiers produce no valid plates, thin response has results=[]."""
    mock_yolo.return_value = DetectionResult(vehicles=[])
    mock_fast_ff.return_value = []
    mock_rapid_ff.return_value = []

    resp = recognize_plate_image(sample_image_bytes, filename="empty_road.jpg")

    assert resp.results == []
    assert resp.execution_time_ms > 0


def test_plate_resolver_preserves_valid_gt_series():
    """Verify that legitimate series like GT in RJ14GT4976 are not mutated to GJ."""
    from app.services.plate_rules import resolve_plate_from_text

    assert resolve_plate_from_text("RJ14GT4976") == "RJ14GT4976"


def test_plate_resolver_corrects_g3_digit_misread():
    """Verify that digit-in-series OCR error G3 and prefix RT are corrected to RJ14GJ4976."""
    from app.services.plate_rules import resolve_plate_from_text

    assert resolve_plate_from_text("RT14G34976") == "RJ14GJ4976"


def test_plate_resolver_filters_decals_and_phones():
    """Verify that commercial decal words and driver phone numbers are rejected."""
    from app.services.plate_rules import resolve_plate_from_text

    assert resolve_plate_from_text("FASTAG") is None
    assert resolve_plate_from_text("GOODSCARRIER") is None
    assert resolve_plate_from_text("9414378858") is None
    assert resolve_plate_from_text("PASSING") is None


@patch("app.services.pipeline.orchestrator.run_fast_alpr_pipeline")
@patch("app.services.pipeline.orchestrator._scan_fast_alpr_crops")
@patch("app.services.pipeline.VehicleDetector.detect")
def test_cascade_stage_logging(mock_yolo, mock_fast_crop, mock_fast_ff, sample_image_bytes):
    """Verify that stage and tier logging are emitted with [pipeline] prefix."""
    from app.core.logging import logger

    mock_yolo.return_value = DetectionResult(
        vehicles=[DetectedVehicle(vehicle_type="car", box=(10, 10, 50, 50), crop=Image.new("RGB", (40, 40)))]
    )
    mock_fast_crop.return_value = [PlateResult(plate="RJ09GA0165", vehicle_box=(10, 10, 50, 50))]

    captured: list[str] = []
    sink_id = logger.add(captured.append, format="{message}")
    try:
        recognize_plate_image(sample_image_bytes, filename="log_test.jpg")
        assert any("[pipeline] Starting ANPR for 'log_test.jpg'" in msg for msg in captured)
        assert any("[pipeline] Stage 1: Detected 1 vehicle(s)" in msg for msg in captured)
        assert any("[pipeline] Tier 1: Scanning 1 vehicle crop(s) via Fast-ALPR" in msg for msg in captured)
        assert any("[pipeline] Tier 1 matched 1 plate(s): ['RJ09GA0165']" in msg for msg in captured)
        assert any("[pipeline] Finished ANPR for 'log_test.jpg': 1 plate(s) found" in msg for msg in captured)
    finally:
        logger.remove(sink_id)

