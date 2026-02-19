from __future__ import annotations

from pathlib import Path
from typing import Tuple

import pandas as pd

from src.utils.config import load_config


def load_raw_data(
    customers_path: Path | None = None,
    transactions_path: Path | None = None,
    alerts_path: Path | None = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load raw CSVs into DataFrames.
    """
    cfg = load_config()
    base = cfg.data.raw_dir

    customers_csv = customers_path or (base / "customers.csv")
    tx_csv = transactions_path or (base / "transactions.csv")
    alerts_csv = alerts_path or (base / "alerts.csv")

    customers = pd.read_csv(customers_csv)
    transactions = pd.read_csv(tx_csv, parse_dates=["timestamp"])
    alerts = pd.read_csv(alerts_csv)

    return customers, transactions, alerts


__all__ = ["load_raw_data"]

