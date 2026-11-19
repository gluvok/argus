"""
Tests for image decode validation, empty upload rejection, and resolution preservation.
"""

import pytest

from app.core.exceptions import InvalidImageError
from app.services.image_processing import decode_image
from app.services.pipeline import recognize_plate_image
from tests.conftest import create_test_jpeg as _jpeg


def test_empty_upload_is_rejected():
    with pytest.raises(InvalidImageError):
        recognize_plate_image(b"", filename="empty.jpg")


def test_full_resolution_image_is_not_modified():
    """1920x1080 (camera native resolution) must pass through without modification."""
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


@pytest.mark.anyio
async def test_read_upload_stream_accepts_valid_payload():
    """Verify stream reading succeeds directly."""
    import io

    from app.services.image_processing.security import read_upload_stream

    class ValidStream:
        def __init__(self, data: bytes):
            self.buf = io.BytesIO(data)

        async def read(self, size: int = -1) -> bytes:
            return self.buf.read(size)

    payload = b"TEST_IMAGE_BYTES"
    result = await read_upload_stream(ValidStream(payload))
    assert result == payload


@pytest.mark.anyio
async def test_read_upload_stream_rejects_empty():
    """Verify stream reading rejects empty payload."""

    from app.services.image_processing.security import read_upload_stream

    class EmptyStream:
        async def read(self, size: int = -1) -> bytes:
            return b""

    with pytest.raises(InvalidImageError):
        await read_upload_stream(EmptyStream())
