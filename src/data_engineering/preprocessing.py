from __future__ import annotations

from typing import Tuple

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def split_train_test(
    features: pd.DataFrame,
    label_column: str | None = None,
    test_size: float = 0.2,
    random_state: int = 42,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series | None, pd.Series | None]:
    """
    Split features (and optional labels) into train and test sets.
    """
    if label_column and label_column in features.columns:
        X = features.drop(columns=[label_column])
        y = features[label_column]
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        return X_train, X_test, y_train, y_test
    else:
        X_train, X_test = train_test_split(
            features, test_size=test_size, random_state=random_state
        )
        return X_train, X_test, None, None


def scale_features(X_train: pd.DataFrame, X_test: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame, StandardScaler]:
    """
    Standardize numeric features using sklearn's StandardScaler.
    """
    scaler = StandardScaler()
    numeric_cols = X_train.select_dtypes(include=["number"]).columns
    X_train_scaled = X_train.copy()
    X_test_scaled = X_test.copy()

    X_train_scaled[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
    X_test_scaled[numeric_cols] = scaler.transform(X_test[numeric_cols])

    return X_train_scaled, X_test_scaled, scaler


__all__ = ["split_train_test", "scale_features"]

