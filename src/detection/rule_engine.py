from __future__ import annotations

from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class RuleResult:
    rule_id: str
    description: str
    triggered_customers: List[str]


def apply_rules(features: pd.DataFrame) -> List[RuleResult]:
    """
    Apply a small set of deterministic AML-style rules at customer level.
    """
    results: List[RuleResult] = []

    # Example thresholds – in real systems, these come from config or DB
    high_total_threshold = 100_000
    high_deviation_threshold = features["deviation_score"].quantile(0.98)

    # Rule 1: unusually high total volume
    r1_mask = features["total_amount"] > high_total_threshold
    results.append(
        RuleResult(
            rule_id="R1_HIGH_VOLUME",
            description="Total transaction volume above configured threshold.",
            triggered_customers=features.loc[r1_mask, "customer_id"].tolist(),
        )
    )

    # Rule 2: high deviation score
    r2_mask = features["deviation_score"] > high_deviation_threshold
    results.append(
        RuleResult(
            rule_id="R2_BEHAVIOR_DEVIATION",
            description="Transaction behaviour significantly deviates from peers.",
            triggered_customers=features.loc[r2_mask, "customer_id"].tolist(),
        )
    )

    return results


def rules_to_frame(results: List[RuleResult]) -> pd.DataFrame:
    """
    Convert rule results to a long-form DataFrame.
    """
    records = []
    for r in results:
        for cust_id in r.triggered_customers:
            records.append(
                {
                    "customer_id": cust_id,
                    "rule_id": r.rule_id,
                    "description": r.description,
                }
            )
    return pd.DataFrame(records)


__all__ = ["RuleResult", "apply_rules", "rules_to_frame"]

