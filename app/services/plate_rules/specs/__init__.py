"""Specification Pattern for candidate vehicle plate validation."""

from app.services.plate_rules.specs.composite import (
    STANDARD_PLATE_SPEC,
    CompositePlateSpec,
)
from app.services.plate_rules.specs.decal import NonDecalSpec
from app.services.plate_rules.specs.format import IndianPlateFormatSpec
from app.services.plate_rules.specs.protocol import PlateSpec
from app.services.plate_rules.specs.state_prefix import StatePrefixSpec

__all__ = [
    "STANDARD_PLATE_SPEC",
    "CompositePlateSpec",
    "IndianPlateFormatSpec",
    "NonDecalSpec",
    "PlateSpec",
    "StatePrefixSpec",
]
