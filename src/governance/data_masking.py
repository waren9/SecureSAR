from __future__ import annotations

from typing import Dict, Any

from src.security.pii_masking import mask_pii_fields


def mask_record_for_role(record: Dict[str, Any], role: str) -> Dict[str, Any]:
    """
    Apply masking rules depending on the viewer's role.
    """
    # Analysts see masked PII, Supervisors/Admin may see unmasked depending on policy.
    if role in {"Supervisor", "Admin"}:
        return record
    return mask_pii_fields(record)


__all__ = ["mask_record_for_role"]

