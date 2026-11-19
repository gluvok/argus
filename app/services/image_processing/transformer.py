"""Image validation and decoding."""

from PIL import Image

from app.core.contracts import ensure
from app.core.exceptions import InvalidImageError
from app.services.image_processing.loader import load_rgb


def decode_image(image_bytes: bytes) -> Image.Image:
    """Validate uploaded image bytes and decode to full-resolution RGB PIL Image."""
    if not image_bytes:
        raise InvalidImageError("Uploaded image file is empty.")
    pil_img = load_rgb(image_bytes)
    ensure(min(pil_img.size) > 0, "decoded image has zero-size dimension")
    return pil_img
