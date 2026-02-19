from __future__ import annotations

from typing import Dict, Any


INJECTION_KEYWORDS = [
    "ignore previous instructions",
    "override system prompt",
    "bypass guardrails",
]

DISALLOWED_OUTPUT_SNIPPETS = [
    "based on customer ethnicity",
    "race-based",
]


def sanitize_user_input(user_text: str) -> str:
    """
    Very small prompt-injection guard: strips known injection patterns.
    """
    lowered = user_text.lower()
    for kw in INJECTION_KEYWORDS:
        if kw in lowered:
            lowered = lowered.replace(kw, "")
    return lowered


def build_guarded_prompt(system_prompt: str, evidence: Dict[str, Any], user_text: str | None = None) -> str:
    """
    Assemble a guarded prompt from system instructions, structured evidence,
    and optional user input.
    """
    safe_user = sanitize_user_input(user_text or "")
    return (
        f"SYSTEM:\n{system_prompt}\n\n"
        f"EVIDENCE (JSON):\n{evidence}\n\n"
        f"USER_REQUEST:\n{safe_user}\n"
    )


def is_output_policy_compliant(text: str) -> bool:
    """
    Basic content filter for LLM outputs.
    """
    lowered = text.lower()
    for snippet in DISALLOWED_OUTPUT_SNIPPETS:
        if snippet in lowered:
            return False
    return True


__all__ = ["sanitize_user_input", "build_guarded_prompt", "is_output_policy_compliant"]

