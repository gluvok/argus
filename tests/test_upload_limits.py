"""
Tests for payload budgets, pixel caps, and image decode validation.
"""

import pytest

from app.core.exceptions import InvalidImageError
from app.services.image_processing import decode_image
from app.services.pipeline import recognize_plate_image
from tests.conftest import create_test_jpeg as _jpeg

# --------------------------------------------------------------------------
# Upload validation
# --------------------------------------------------------------------------


def test_empty_upload_is_rejected():
    with pytest.raises(InvalidImageError):
        recognize_plate_image(b"", filename="empty.jpg")


# --------------------------------------------------------------------------
# Image decode & resolution
# --------------------------------------------------------------------------


def test_full_resolution_image_is_not_modified():
    """1920x1080 (camera native resolution) must pass through without any modification."""
    from PIL import Image

    out = decode_image(_jpeg(1920, 1080))
    assert isinstance(out, Image.Image)
    assert out.size == (1920, 1080)


def test_small_image_is_not_upscaled():
    from PIL import Image

    out = decode_image(_jpeg(320, 240))
    assert isinstance(out, Image.Image)
    assert out.size == (320, 240)


def test_undecodable_bytes_raise_invalid_image():
    with pytest.raises(InvalidImageError):
        decode_image(b"this is not an image")
