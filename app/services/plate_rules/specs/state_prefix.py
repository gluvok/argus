"""State prefix specification matching official Indian State/UT codes."""

from app.services.plate_rules.states import STATE_CODES


class StatePrefixSpec:
    """Ensures state prefix matches one of the official Indian State/UT codes."""

    def is_satisfied_by(self, candidate: str) -> bool:
        return len(candidate) >= 2 and candidate[:2].upper() in STATE_CODES
