"""Tests for OCREngine Strategy Protocol and concrete strategies."""

from unittest.mock import MagicMock, patch

from PIL import Image

from app.schemas import DetectedVehicle, PlateResult
from app.services.ocr.protocol import OCREngine, scan_crops_with_engine
from app.services.ocr.strategies import (
    FastALPROCREngine,
    RapidOCREngine,
)


def test_ocr_engine_protocol_conformance():
    """Verify concrete strategies conform structurally to OCREngine Protocol."""
    fast_alpr = FastALPROCREngine()
    rapid_ocr = RapidOCREngine()

    assert isinstance(fast_alpr, OCREngine)
    assert isinstance(rapid_ocr, OCREngine)
    assert fast_alpr.name == "Fast-ALPR"
    assert rapid_ocr.name == "RapidOCR"


def test_strategy_scan_crops_with_mock_engine():
    """Verify generic crop scanner loops over vehicles and respects early exit."""
    mock_engine = MagicMock(spec=OCREngine)
    v1 = DetectedVehicle(vehicle_type="car", box=(0, 0, 100, 100), crop=Image.new("RGB", (50, 50)))
    v2 = DetectedVehicle(vehicle_type="truck", box=(0, 0, 80, 80), crop=Image.new("RGB", (50, 50)))

    mock_engine.scan_vehicle.side_effect = [
        [PlateResult(plate="DL01AB1234", vehicle_box=(0, 0, 100, 100))],
        [PlateResult(plate="HR26CD5678", vehicle_box=(0, 0, 80, 80))],
    ]

    # Single vehicle exit (default setting: ENABLE_MULTI_VEHICLE_OCR = False)
    with patch("app.core.config.settings.ENABLE_MULTI_VEHICLE_OCR", False):
        results = scan_crops_with_engine(mock_engine, [v1, v2])
        assert len(results) == 1
        assert results[0].plate == "DL01AB1234"
        assert mock_engine.scan_vehicle.call_count == 1

    # Multi vehicle scan (ENABLE_MULTI_VEHICLE_OCR = True)
    mock_engine.reset_mock()
    mock_engine.scan_vehicle.side_effect = [
        [PlateResult(plate="DL01AB1234", vehicle_box=(0, 0, 100, 100))],
        [PlateResult(plate="HR26CD5678", vehicle_box=(0, 0, 80, 80))],
    ]
    with patch("app.core.config.settings.ENABLE_MULTI_VEHICLE_OCR", True):
        results = scan_crops_with_engine(mock_engine, [v1, v2])
        assert len(results) == 2
        assert mock_engine.scan_vehicle.call_count == 2
