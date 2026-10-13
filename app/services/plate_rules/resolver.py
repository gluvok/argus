"""Unified raw OCR text normalization, decal filtering, and plate validation."""

from app.services.plate_rules.expander import normalize_candidate_strings
from app.services.plate_rules.parser import parse_plate_info
from app.services.plate_rules.specs import NonDecalSpec


def resolve_plate_from_text(raw_text: str | None) -> str | None:
    """Filter decals, normalize common OCR confusions, and validate Indian plate."""
    if not raw_text or not NonDecalSpec().is_satisfied_by(raw_text):
        return None
    for cand in normalize_candidate_strings(raw_text):
        if (info := parse_plate_info(cand)) and (p := info.get("plate")):
            return p
    return None
