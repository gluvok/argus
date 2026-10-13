"""Indian plate format specification matching State Series syntax."""

from app.services.plate_rules.states import INDIAN_PLATE_REGEX


class IndianPlateFormatSpec:
    """Ensures registration format matches standard Indian State Series syntax."""

    def is_satisfied_by(self, candidate: str) -> bool:
        return bool(INDIAN_PLATE_REGEX.fullmatch(candidate))
