"""Composite plate specification combining multiple rules."""

from app.services.plate_rules.specs.format import IndianPlateFormatSpec
from app.services.plate_rules.specs.protocol import PlateSpec
from app.services.plate_rules.specs.state_prefix import StatePrefixSpec


class CompositePlateSpec:
    """Composite Specification requiring all encapsulated specs to be satisfied."""

    def __init__(self, *specs: PlateSpec) -> None:
        self.specs = specs

    def is_satisfied_by(self, candidate: str) -> bool:
        return all(s.is_satisfied_by(candidate) for s in self.specs)


STANDARD_PLATE_SPEC = CompositePlateSpec(StatePrefixSpec(), IndianPlateFormatSpec())
