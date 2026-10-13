"""Specification Pattern for candidate vehicle plate validation."""

from typing import Protocol, runtime_checkable

from app.services.plate_rules.filters import is_decal_word, is_phone_number
from app.services.plate_rules.states import INDIAN_PLATE_REGEX, STATE_CODES


@runtime_checkable
class PlateSpec(Protocol):
    """Specification Protocol for candidate plate validation."""

    def is_satisfied_by(self, candidate: str) -> bool:
        """Return True if candidate satisfies the specification."""
        ...


class NonDecalSpec:
    """Ensures candidate text is neither a commercial decal nor a phone number."""

    def is_satisfied_by(self, candidate: str) -> bool:
        return not (is_decal_word(candidate) or is_phone_number(candidate))


class StatePrefixSpec:
    """Ensures state prefix matches one of the official Indian State/UT codes."""

    def is_satisfied_by(self, candidate: str) -> bool:
        return len(candidate) >= 2 and candidate[:2].upper() in STATE_CODES


class IndianPlateFormatSpec:
    """Ensures registration format matches standard Indian State Series syntax."""

    def is_satisfied_by(self, candidate: str) -> bool:
        return bool(INDIAN_PLATE_REGEX.fullmatch(candidate))


class CompositePlateSpec:
    """Composite Specification requiring all encapsulated specs to be satisfied."""

    def __init__(self, *specs: PlateSpec) -> None:
        self.specs = specs

    def is_satisfied_by(self, candidate: str) -> bool:
        return all(s.is_satisfied_by(candidate) for s in self.specs)


STANDARD_PLATE_SPEC = CompositePlateSpec(StatePrefixSpec(), IndianPlateFormatSpec())
