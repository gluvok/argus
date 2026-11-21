"""Image validation, decoding, and decompression bomb guard."""

from PIL import Image

from app.core.contracts import ensure
from app.services.image_processing.loader import load_rgb
from app.services.image_processing.security import probe_image


def decode_image(image_bytes: bytes) -> Image.Image:
    """Validate an uploaded image and decode it to a full-resolution RGB PIL Image."""
    probe_image(image_bytes)
    pil_img = load_rgb(image_bytes)
    ensure(min(pil_img.size) > 0, "decoded image has zero-size dimension")
    return pil_img
