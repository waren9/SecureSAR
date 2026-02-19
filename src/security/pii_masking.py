from __future__ import annotations

from typing import Dict, Any
import hashlib


PII_FIELDS = {"account_number", "pan", "aadhaar", "phone", "address"}


def _tokenize(value: str) -> str:
    """
    Deterministically hash PII values to opaque tokens.
    """
    h = hashlib.sha256(value.encode("utf-8")).hexdigest()[:12]
    return f"TOK_{h}"


def mask_pii_fields(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Return a copy of the record with PII fields tokenized.
    """
    masked = dict(record)
    for field in PII_FIELDS:
        if field in masked and masked[field] is not None:
            masked[field] = _tokenize(str(masked[field]))
    return masked


__all__ = ["PII_FIELDS", "mask_pii_fields"]

