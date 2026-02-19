from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.utils.config import load_config
from src.utils.helpers import ensure_dir


def engineer_features(
    customers: pd.DataFrame,
    transactions: pd.DataFrame,
) -> pd.DataFrame:
    """
    Create customer-level behavioural features from raw transactions.
    """
    # Total amount and count over 7 days
    tx_sorted = transactions.sort_values("timestamp")
    tx_sorted["date"] = tx_sorted["timestamp"].dt.date

    agg = (
        tx_sorted.groupby("customer_id")
        .agg(
            total_amount=("amount", "sum"),
            tx_count=("transaction_id", "count"),
            avg_amount=("amount", "mean"),
        )
        .reset_index()
    )

    # Join static customer attributes
    features = customers.merge(agg, on="customer_id", how="left")
    features[["total_amount", "tx_count", "avg_amount"]] = features[
        ["total_amount", "tx_count", "avg_amount"]
    ].fillna(0)

    # Simple deviation proxy: log(total_amount + 1)
    features["deviation_score"] = (features["total_amount"] + 1).apply(lambda x: float(pd.np.log(x)))

    return features


def save_features(df: pd.DataFrame, path: Path | None = None) -> Path:
    """
    Persist engineered features to data/processed.
    """
    cfg = load_config()
    out_path = path or (cfg.data.processed_dir / "feature_engineered.csv")
    ensure_dir(out_path.parent)
    df.to_csv(out_path, index=False)
    return out_path


__all__ = ["engineer_features", "save_features"]

