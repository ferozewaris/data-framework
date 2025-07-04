"""Cleansing transformations for the Silver layer."""

from __future__ import annotations

import pandas as pd
from typing import Any, Dict
from utils import read_yaml


def clean_data(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """Apply cleaning rules from the configuration."""
    rules = config.get("cleaning", {})
    for col, ops in rules.items():
        if "fillna" in ops:
            df[col] = df[col].fillna(ops["fillna"])
        if ops.get("dropna"):
            df = df[df[col].notna()]
        if "astype" in ops:
            df[col] = df[col].astype(ops["astype"])
        if ops.get("lowercase"):
            df[col] = df[col].str.lower()
    if config.get("deduplicate"):
        df = df.drop_duplicates()
    return df


def load_and_clean(csv_path: str, config_path: str) -> pd.DataFrame:
    """Convenience function to load config and clean data."""
    cfg = read_yaml(config_path)
    df = pd.read_csv(csv_path)
    return clean_data(df, cfg)

