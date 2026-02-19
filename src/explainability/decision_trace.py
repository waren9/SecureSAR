from __future__ import annotations

from typing import Any, Dict, List

import numpy as np
import pandas as pd
from sklearn.tree import _tree


def extract_decision_path(model: Any, X: pd.DataFrame, sample_index: int) -> List[Dict[str, str]]:
    """
    Extract a human-readable decision path for a single sample from a tree-based model.
    """
    if not hasattr(model, "tree_"):
        raise TypeError("Model does not expose a sklearn-style tree_.")

    tree = model.tree_
    feature_names = np.array(X.columns)

    node_indicator = model.decision_path(X)
    leave_id = model.apply(X)
    sample_id = sample_index

    node_index = node_indicator.indices[
        node_indicator.indptr[sample_id] : node_indicator.indptr[sample_id + 1]
    ]

    path: List[Dict[str, str]] = []
    for node_id in node_index:
        if leave_id[sample_id] == node_id:
            continue
        feature = feature_names[tree.feature[node_id]]
        threshold = tree.threshold[node_id]
        if X.iloc[sample_id, tree.feature[node_id]] <= threshold:
            rule = f"{feature} <= {threshold:.3f}"
        else:
            rule = f"{feature} > {threshold:.3f}"
        path.append({"node_id": str(node_id), "rule": rule})

    return path


__all__ = ["extract_decision_path"]

