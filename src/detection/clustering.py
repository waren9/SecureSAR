from __future__ import annotations

from typing import Tuple

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE


def embed_and_cluster(features: pd.DataFrame, n_clusters: int = 5) -> Tuple[pd.DataFrame, KMeans]:
    """
    Simple t-SNE embedding followed by KMeans clustering on numeric features.
    """
    numeric = features.select_dtypes(include=["number"])
    if numeric.empty:
        raise ValueError("No numeric features available for clustering.")

    tsne = TSNE(n_components=2, random_state=42, init="random", learning_rate="auto")
    embedding = tsne.fit_transform(numeric)

    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init="auto")
    cluster_labels = kmeans.fit_predict(embedding)

    out = features.copy()
    out["cluster"] = cluster_labels
    out["tsne_x"] = embedding[:, 0]
    out["tsne_y"] = embedding[:, 1]

    return out, kmeans


__all__ = ["embed_and_cluster"]

