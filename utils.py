"""Utility functions for the Gen-AI data pipeline."""

from __future__ import annotations

import logging
from typing import Any, Dict
import yaml
import pandas as pd


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def read_yaml(path: str) -> Dict[str, Any]:
    """Read YAML configuration from a file."""
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def write_yaml(data: Dict[str, Any], path: str) -> None:
    """Write YAML configuration to a file."""
    with open(path, "w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, sort_keys=False)


def detect_schema(csv_path: str, sample_rows: int = 100) -> Dict[str, str]:
    """Infer a simple schema from a CSV file."""
    df_sample = pd.read_csv(csv_path, nrows=sample_rows)
    schema = {col: str(dtype) for col, dtype in df_sample.dtypes.items()}
    logger.info("Detected schema: %s", schema)
    return schema

