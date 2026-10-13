"""Non-decal specification rejecting commercial decals and phone numbers."""

from app.services.plate_rules.filters import is_decal_word, is_phone_number


class NonDecalSpec:
    """Ensures candidate text is neither a commercial decal nor a phone number."""

    def is_satisfied_by(self, candidate: str) -> bool:
        return not (is_decal_word(candidate) or is_phone_number(candidate))
