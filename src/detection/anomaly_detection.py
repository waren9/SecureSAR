from __future__ import annotations

from typing import Tuple

import pandas as pd
from sklearn.ensemble import IsolationForest

from src.utils.config import load_config


def fit_isolation_forest(features: pd.DataFrame) -> Tuple[IsolationForest, pd.Series]:
    """
    Fit an IsolationForest on numeric features and return model and anomaly scores.
    """
    cfg = load_config()
    numeric = features.select_dtypes(include=["number"])
    model = IsolationForest(
        contamination=cfg.model.isolation_forest_contamination,
        random_state=cfg.data.synthetic_seed,
    )
    model.fit(numeric)
    scores = -model.decision_function(numeric)  # higher = more anomalous
    return model, pd.Series(scores, index=features.index, name="anomaly_score")


__all__ = ["fit_isolation_forest"]

