"""Tests for scripts.benchmark utilities."""

import os
import tempfile
from pathlib import Path

from scripts.benchmark import natural_key, serialize_images


def test_benchmark_natural_key_sorting():
    files = ["10.jpg", "1.jpg", "2.jpg", "20.jpg"]
    sorted_files = sorted(files, key=natural_key)
    assert sorted_files == ["1.jpg", "2.jpg", "10.jpg", "20.jpg"]


def test_benchmark_serialize_images_is_read_only(tmp_path: Path):
    """Verify serialize_images returns sorted paths and does not rename files."""
    f1 = tmp_path / "2.jpg"
    f2 = tmp_path / "1.jpg"
    f1.write_bytes(b"image2")
    f2.write_bytes(b"image1")

    paths = serialize_images(str(tmp_path))
    assert [os.path.basename(p) for p in paths] == ["1.jpg", "2.jpg"]
    assert f1.exists()
    assert f2.exists()
