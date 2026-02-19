from __future__ import annotations

import pandas as pd


def validate_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic quality checks on customers.
    """
    df = df.drop_duplicates(subset=["customer_id"])
    df = df.dropna(subset=["customer_id"])
    return df


def validate_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic quality checks on transactions.
    """
    df = df.dropna(subset=["transaction_id", "customer_id", "amount"])
    df = df[df["amount"] > 0]
    df = df.drop_duplicates(subset=["transaction_id"])
    return df


def validate_alerts(df: pd.DataFrame) -> pd.DataFrame:
    """
    Basic quality checks on alerts.
    """
    df = df.dropna(subset=["alert_id", "transaction_id", "customer_id"])
    df = df.drop_duplicates(subset=["alert_id"])
    return df


__all__ = ["validate_customers", "validate_transactions", "validate_alerts"]

