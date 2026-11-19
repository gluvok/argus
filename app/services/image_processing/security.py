"""Image security checks and upload handling."""

from typing import Any

from app.core.exceptions import InvalidImageError


async def read_upload_stream(file: Any) -> bytes:
    """Read upload file bytes directly, rejecting empty uploads."""
    data = await file.read()
    if not data:
        raise InvalidImageError("Uploaded image file is empty.")
    return data


def validate_image_upload(image_bytes: bytes, content_type: str | None = None) -> None:
    """Validate image bytes are present."""
    if not image_bytes:
        raise InvalidImageError("Uploaded image file is empty.")
