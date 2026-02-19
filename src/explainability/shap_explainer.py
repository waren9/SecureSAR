from __future__ import annotations

from typing import Any, Tuple

import numpy as np
import pandas as pd
import shap


def compute_shap_values(model: Any, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
    """
    Compute SHAP values for a fitted tree-based model on the given features.

    Returns:
      - shap_values: array of SHAP values (n_samples, n_features)
      - expected_value: array of expected values (per output)
    """
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X)
    expected_value = np.atleast_1d(explainer.expected_value)
    # For binary classification, shap_values may be a list; use the last element
    if isinstance(shap_values, list):
        shap_values = shap_values[-1]
    return np.asarray(shap_values), expected_value


__all__ = ["compute_shap_values"]

