from __future__ import annotations

from typing import Set


ROLE_PERMISSIONS = {
    "Analyst": {
        "view_cases",
        "view_masked_pii",
        "edit_sar_draft",
    },
    "Supervisor": {
        "view_cases",
        "view_masked_pii",
        "view_unmasked_pii",
        "approve_sar",
    },
    "Admin": {
        "view_cases",
        "view_unmasked_pii",
        "configure_rules",
        "configure_models",
        "manage_users",
    },
    "Regulator": {
        "view_cases",
        "view_audit_logs",
    },
}


def has_permission(role: str, permission: str) -> bool:
    """
    Check whether a given role has the requested permission.
    """
    perms: Set[str] = ROLE_PERMISSIONS.get(role, set())
    return permission in perms


__all__ = ["ROLE_PERMISSIONS", "has_permission"]

