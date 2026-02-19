from __future__ import annotations

from typing import List, Dict

import pandas as pd


def map_to_typologies(rules_df: pd.DataFrame, anomaly_scores: pd.Series) -> List[Dict[str, str]]:
    """
    Map rule triggers and anomaly scores to human-readable AML typologies.
    """
    typologies: List[Dict[str, str]] = []
    high_anomaly_customers = anomaly_scores[anomaly_scores > anomaly_scores.quantile(0.98)].index

    for cust_id in high_anomaly_customers:
        cust_rules = rules_df[rules_df["customer_id"] == cust_id]["rule_id"].unique().tolist()
        if "R1_HIGH_VOLUME" in cust_rules:
            typology = "Structuring / high volume anomaly"
        elif "R2_BEHAVIOR_DEVIATION" in cust_rules:
            typology = "Behavioural deviation from peer group"
        else:
            typology = "Unusual behaviour (unspecified)"

        typologies.append(
            {
                "customer_id": str(cust_id),
                "typology": typology,
            }
        )
    return typologies


__all__ = ["map_to_typologies"]

