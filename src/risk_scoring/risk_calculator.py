from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Tuple

import pandas as pd
import yaml

from src.utils.config import load_config
from src.utils.helpers import ensure_dir


def load_score_weights(path: Path | None = None) -> Dict[str, float]:
    """
    Load risk score weights and thresholds from YAML.
    """
    cfg = load_config()
    weights_path = path or cfg.risk.score_weights_path
    if not weights_path.exists():
        # Fall back to sensible defaults
        return {
            "rule_weight": 0.5,
            "anomaly_weight": 0.3,
            "cluster_weight": 0.2,
            "high_risk_threshold": 0.8,
        }
    with weights_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return {
        "rule_weight": float(data.get("rule_weight", 0.5)),
        "anomaly_weight": float(data.get("anomaly_weight", 0.3)),
        "cluster_weight": float(data.get("cluster_weight", 0.2)),
        "high_risk_threshold": float(data.get("high_risk_threshold", 0.8)),
    }


def compute_risk_scores(
    features: pd.DataFrame,
    rules_df: pd.DataFrame,
    anomaly_scores: pd.Series,
    cluster_df: pd.DataFrame,
    typologies: List[Dict[str, str]],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Combine rule triggers, anomaly scores, clusters, and typologies into risk scores.
    Returns:
      - customer-level risk scores DataFrame
      - typology mapping DataFrame
    """
    weights = load_score_weights()

    df = features[["customer_id"]].copy()
    df = df.drop_duplicates(subset=["customer_id"])

    # Rule component: count of triggered rules per customer, min-max normalized
    if not rules_df.empty:
        rule_counts = rules_df.groupby("customer_id")["rule_id"].nunique()
        rule_scores = (rule_counts - rule_counts.min()) / (rule_counts.max() - rule_counts.min() or 1.0)
    else:
        rule_scores = pd.Series(0.0, index=df["customer_id"])

    # Anomaly component: already a score; min-max normalize
    if not anomaly_scores.empty:
        a_min = anomaly_scores.min()
        a_max = anomaly_scores.max()
        anomaly_norm = (anomaly_scores - a_min) / (a_max - a_min or 1.0)
    else:
        anomaly_norm = pd.Series(0.0, index=df.index)

    # Cluster component: mark clusters that appear high-risk (simple heuristic)
    high_risk_clusters = (
        cluster_df.groupby("cluster")["total_amount"].mean().sort_values(ascending=False).head(2).index
        if not cluster_df.empty
        else []
    )
    cluster_scores = cluster_df.set_index("customer_id")["cluster"].map(
        lambda c: 1.0 if c in high_risk_clusters else 0.0
    )

    df = df.set_index("customer_id")
    df["rule_score"] = rule_scores.reindex(df.index).fillna(0.0)
    df["anomaly_score"] = anomaly_norm.reindex(df.index).fillna(0.0)
    df["cluster_score"] = cluster_scores.reindex(df.index).fillna(0.0)

    df["risk_score"] = (
        weights["rule_weight"] * df["rule_score"]
        + weights["anomaly_weight"] * df["anomaly_score"]
        + weights["cluster_weight"] * df["cluster_score"]
    )

    df["risk_band"] = pd.cut(
        df["risk_score"],
        bins=[-0.01, 0.3, 0.6, 1.0],
        labels=["Low", "Medium", "High"],
    )

    # Typologies
    typology_df = pd.DataFrame(typologies) if typologies else pd.DataFrame(columns=["customer_id", "typology"])

    df = df.reset_index()
    return df, typology_df


def save_risk_scores(df: pd.DataFrame, path: Path | None = None) -> Path:
    """
    Persist risk scores to data/processed.
    """
    cfg = load_config()
    out_path = path or (cfg.data.processed_dir / "risk_scores.csv")
    ensure_dir(out_path.parent)
    df.to_csv(out_path, index=False)
    return out_path


__all__ = ["load_score_weights", "compute_risk_scores", "save_risk_scores"]

