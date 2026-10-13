"""Specification Protocol for candidate plate validation."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class PlateSpec(Protocol):
    """Specification Protocol for candidate plate validation."""

    def is_satisfied_by(self, candidate: str) -> bool:
        """Return True if candidate satisfies the specification."""
        ...
