"""
Tests for payload budgets, pixel caps, and image decode validation.
"""

import pytest

from app.core.constants import MAX_UPLOAD_BYTES
from app.core.exceptions import InvalidImageError, PayloadTooLargeError
from app.services.image_processing import decode_image
from app.services.pipeline import recognize_plate_image
from tests.conftest import create_test_jpeg as _jpeg

# --------------------------------------------------------------------------
# Upload size & limits
# --------------------------------------------------------------------------


def test_oversized_upload_is_rejected():
    oversized = b"\xff\xd8\xff\xe0" + b"\x00" * (MAX_UPLOAD_BYTES + 1024)
    with pytest.raises(PayloadTooLargeError):
        recognize_plate_image(oversized, filename="huge.jpg")


def test_empty_upload_is_rejected():
    with pytest.raises(InvalidImageError):
        recognize_plate_image(b"", filename="empty.jpg")


# --------------------------------------------------------------------------
# Decode bombs and pixel cap
# --------------------------------------------------------------------------


def test_pixel_budget_is_enforced(monkeypatch):
    """
    A small file can declare enormous dimensions. Guard on the pixel count from
    the header, before the full decode allocates anything.
    """
    monkeypatch.setattr(
        "app.services.image_processing.transformer.MAX_IMAGE_PIXELS", 1000
    )
    with pytest.raises(PayloadTooLargeError):
        decode_image(_jpeg(200, 200))


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


# --------------------------------------------------------------------------
# Streaming chunked upload guard
# --------------------------------------------------------------------------


@pytest.mark.anyio
async def test_read_upload_stream_rejects_oversized_chunked():
    """Verify stream reading halts and raises PayloadTooLargeError without buffering full payload."""
    from app.services.image_processing.security import read_upload_stream

    class MockStream:
        def __init__(self, size_bytes: int):
            self.remaining = size_bytes
            self.chunk_size = 64 * 1024

        async def read(self, size: int = -1) -> bytes:
            if self.remaining <= 0:
                return b""
            to_read = min(self.chunk_size, self.remaining)
            self.remaining -= to_read
            return b"X" * to_read

    # 8MB + 128KB payload stream
    stream = MockStream(8 * 1024 * 1024 + 128 * 1024)
    with pytest.raises(
        PayloadTooLargeError, match="Image exceeds maximum permitted size"
    ):
        await read_upload_stream(stream, max_bytes=8 * 1024 * 1024)


@pytest.mark.anyio
async def test_read_upload_stream_accepts_valid_payload():
    """Verify stream reading succeeds within permitted size limit."""
    import io

    from app.services.image_processing.security import read_upload_stream

    class ValidStream:
        def __init__(self, data: bytes):
            self.buf = io.BytesIO(data)

        async def read(self, size: int = -1) -> bytes:
            return self.buf.read(size)

    payload = b"TEST_IMAGE_BYTES"
    result = await read_upload_stream(ValidStream(payload), max_bytes=1024)
    assert result == payload
