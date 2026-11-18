import pytest

from app.core import constants
from app.core.config import settings
from app.core.exceptions import (
    ANPRServiceError,
    InvalidImageError,
)


def test_settings_default_values():
    assert settings.ENABLE_MULTI_VEHICLE_OCR is False


def test_constants_default_values():
    assert constants.PROJECT_NAME == "Argus ANPR Microservice"
    assert constants.VERSION  # non-empty — exact value varies with installed package
    assert constants.YOLO_MODEL_NAME == "yolo26n_openvino_model"
    assert constants.VEHICLE_CONF_THRESH == 0.35
    assert constants.SERVER_HOST == "127.0.0.1"
    assert constants.SERVER_PORT == 8000


def test_settings_env_loading(monkeypatch):
    from app.core.config import Settings

    monkeypatch.setenv("ENABLE_MULTI_VEHICLE_OCR", "true")

    custom_settings = Settings()
    assert custom_settings.ENABLE_MULTI_VEHICLE_OCR is True


def test_anpr_service_error():
    err = ANPRServiceError("Base error message", status_code=500)
    assert err.message == "Base error message"
    assert err.status_code == 500
    assert str(err) == "Base error message"


def test_invalid_image_error():
    err = InvalidImageError("Unsupported image format")
    assert err.status_code == 400
    assert err.message == "Unsupported image format"


def test_contracts_require_and_ensure():
    from app.core.contracts import ContractViolation, ensure, require

    require(True, "should not raise")
    ensure(True, "should not raise")

    with pytest.raises(ContractViolation, match="precondition failed"):
        require(False, "precondition check failed")

    with pytest.raises(ContractViolation, match="postcondition failed"):
        ensure(False, "postcondition check failed")


def test_contracts_bounded():
    from app.core.bounds import bounded
    from app.core.contracts import ContractViolation

    assert bounded(None, 5, "empty") == []
    assert bounded([1, 2], 5, "small") == [1, 2]
    assert bounded([1, 2, 3, 4], 2, "truncated") == [1, 2]

    with pytest.raises(ContractViolation, match="limit must be positive"):
        bounded([1], 0, "invalid limit")


def test_cors_credentials_not_allowed_with_wildcard():
    """Verify that wildcard CORS does not enable credentials."""
    if "*" in constants.CORS_ORIGINS:
        assert constants.CORS_ALLOW_CREDENTIALS is False, (
            "CORS allow_credentials must be False when allow_origins is wildcard '*'"
        )


def test_pil_max_image_pixels_set_at_constants_import():
    """Verify Image.MAX_IMAGE_PIXELS is configured without needing loader.py imported."""
    import subprocess
    import sys

    code = (
        "from PIL import Image; "
        "import app.core.constants as c; "
        "assert Image.MAX_IMAGE_PIXELS == c.MAX_IMAGE_PIXELS, f'Expected {c.MAX_IMAGE_PIXELS}, got {Image.MAX_IMAGE_PIXELS}'"
    )
    result = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, check=False
    )
    assert result.returncode == 0, result.stderr


def test_app_package_exports():
    """Verify top-level package exports app and recognize_plate_image lazily."""
    from fastapi import FastAPI

    from app import app as fastapi_app
    from app import recognize_plate_image

    assert isinstance(fastapi_app, FastAPI)
    assert callable(recognize_plate_image)
