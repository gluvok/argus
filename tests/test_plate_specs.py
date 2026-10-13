"""Unit tests for the Specification Pattern plate validation rules."""

from app.services.plate_rules.specs import (
    STANDARD_PLATE_SPEC,
    CompositePlateSpec,
    IndianPlateFormatSpec,
    NonDecalSpec,
    PlateSpec,
    StatePrefixSpec,
)


def test_plate_spec_protocol_conformance():
    """Verify concrete specifications conform structurally to PlateSpec."""
    assert isinstance(NonDecalSpec(), PlateSpec)
    assert isinstance(StatePrefixSpec(), PlateSpec)
    assert isinstance(IndianPlateFormatSpec(), PlateSpec)
    assert isinstance(STANDARD_PLATE_SPEC, PlateSpec)


def test_non_decal_spec():
    spec = NonDecalSpec()
    assert spec.is_satisfied_by("MH12AB1234") is True
    assert spec.is_satisfied_by("GOODS CARRIER") is False
    assert spec.is_satisfied_by("9876543210") is False


def test_state_prefix_spec():
    spec = StatePrefixSpec()
    assert spec.is_satisfied_by("DL01AB1234") is True
    assert spec.is_satisfied_by("RJ09GA0165") is True
    assert spec.is_satisfied_by("ZZ01AB1234") is False
    assert spec.is_satisfied_by("A") is False


def test_indian_plate_format_spec():
    spec = IndianPlateFormatSpec()
    assert spec.is_satisfied_by("DL01AB1234") is True
    assert spec.is_satisfied_by("RJ09GA0165") is True
    assert spec.is_satisfied_by("INVALID123") is False


def test_composite_plate_spec():
    composite = CompositePlateSpec(StatePrefixSpec(), IndianPlateFormatSpec())
    assert composite.is_satisfied_by("DL01AB1234") is True
    assert composite.is_satisfied_by("ZZ01AB1234") is False
    assert composite.is_satisfied_by("INVALID") is False
