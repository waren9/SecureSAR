from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict

import boto3

from src.utils.config import load_config


def _load_prompt_template() -> str:
    path = Path(__file__).with_name("prompt_template.txt")
    return path.read_text(encoding="utf-8")


@dataclass
class NarrativeGenerator:
    """
    Generates SAR narratives from structured evidence.

    In production, this can call Amazon Bedrock; in local/dev mode, it falls
    back to a deterministic template-based narrative.
    """

    use_real_llm: bool = False

    def __post_init__(self) -> None:
        self.cfg = load_config()
        self.template = _load_prompt_template()
        self._bedrock = None
        if self.use_real_llm or self.cfg.llm.use_real_llm:
            self._bedrock = boto3.client(
                "bedrock-runtime",
                region_name=self.cfg.llm.region_name,
            )

    def _call_bedrock(self, evidence: Dict[str, Any]) -> str:
        if self._bedrock is None:
            raise RuntimeError("Bedrock client not configured.")
        prompt = {
            "system": self.template,
            "evidence": evidence,
        }
        # NOTE: This is a minimal placeholder; adapt to actual Bedrock model schema.
        response = self._bedrock.invoke_model(
            modelId=self.cfg.llm.bedrock_model_id,
            body=str(prompt).encode("utf-8"),
        )
        body = response.get("body")
        text = body.read().decode("utf-8") if hasattr(body, "read") else str(body)
        return text

    def _deterministic_narrative(self, evidence: Dict[str, Any]) -> str:
        """
        Fallback when no real LLM is configured – uses a simple string template.
        """
        customer_id = evidence.get("customer_id", "UNKNOWN_CUSTOMER")
        risk_score = evidence.get("risk_score", "N/A")
        typologies = ", ".join(evidence.get("typologies", [])) or "Unspecified typology"
        rules = ", ".join(evidence.get("triggered_rules", [])) or "No deterministic rules triggered"

        return (
            f"Summary of suspicious activity:\n"
            f"Customer {customer_id} has been identified as potentially high risk with a risk score of {risk_score}.\n\n"
            f"Description of activity and patterns observed:\n"
            f"The customer exhibits behaviour consistent with the following typologies: {typologies}.\n"
            f"Deterministic rules triggered: {rules}.\n\n"
            f"Risk rationale:\n"
            f"This narrative has been generated using the SecureSAR decision framework and is intended as a draft for human review.\n"
        )

    def generate(self, evidence: Dict[str, Any]) -> str:
        """
        Generate a SAR narrative string from structured evidence.
        """
        if self._bedrock is not None:
            try:
                return self._call_bedrock(evidence)
            except Exception:
                # Fallback for local runs or misconfiguration
                return self._deterministic_narrative(evidence)
        return self._deterministic_narrative(evidence)


__all__ = ["NarrativeGenerator"]

