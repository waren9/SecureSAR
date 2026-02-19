from __future__ import annotations

from typing import Set

from src.governance.role_based_access import ROLE_PERMISSIONS


def get_permissions_for_role(role: str) -> Set[str]:
    """
    Return the set of permissions for a given role.
    """
    return ROLE_PERMISSIONS.get(role, set())


def can_edit_sar(role: str) -> bool:
    return "edit_sar_draft" in get_permissions_for_role(role)


def can_approve_sar(role: str) -> bool:
    return "approve_sar" in get_permissions_for_role(role)


def can_view_unmasked_pii(role: str) -> bool:
    return "view_unmasked_pii" in get_permissions_for_role(role)


__all__ = ["get_permissions_for_role", "can_edit_sar", "can_approve_sar", "can_view_unmasked_pii"]

