"""Aggregation utilities for the Gold layer."""

from __future__ import annotations

import pandas as pd
from typing import Any, Dict


def aggregate_data(df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
    """Aggregate data according to config definitions."""
    aggs = config.get("aggregations", [])
    result = df.copy()
    for agg in aggs:
        group_cols = agg.get("group_by")
        metrics = agg.get("metrics")
        if group_cols and metrics:
            agg_dict = {m["column"]: m["agg"] for m in metrics}
            temp = result.groupby(group_cols).agg(agg_dict).reset_index()
            temp.columns = ["_".join(filter(None, col)) if isinstance(col, tuple) else col for col in temp.columns]
            result = temp
    return result

