from __future__ import annotations

import os


def is_external_call_allowed() -> bool:
    """
    Simple environment-aware toggle for allowing outbound calls (e.g. to Bedrock).
    """
    return os.getenv("SECURESAR_ALLOW_EXTERNAL_CALLS", "false").lower() == "true"


def assert_environment_safe() -> None:
    """
    Placeholder guardrail hook; in real deployments this can enforce:
    - Region restrictions
    - Network segmentation constraints
    - Data residency controls
    """
    # For now this is a no-op suitable for local development.
    return None


__all__ = ["is_external_call_allowed", "assert_environment_safe"]

