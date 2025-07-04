"""Dashboard generation utilities."""

from __future__ import annotations

from typing import Any, Dict, List
import pandas as pd
import plotly.express as px
from utils import write_yaml


def generate_charts(df: pd.DataFrame, specs: List[Dict[str, Any]]) -> List[Any]:
    """Generate Plotly charts based on chart specs."""
    charts = []
    for spec in specs:
        chart_type = spec.get("type")
        if chart_type == "bar":
            fig = px.bar(df, x=spec["x"], y=spec["y"], title=spec.get("title"))
        elif chart_type == "line":
            fig = px.line(df, x=spec["x"], y=spec["y"], title=spec.get("title"))
        elif chart_type == "pie":
            fig = px.pie(df, names=spec["names"], values=spec["values"], title=spec.get("title"))
        else:
            continue
        charts.append(fig)
    return charts


def save_dashboard(charts: List[Any], output_html: str) -> None:
    """Save multiple charts into a single HTML file."""
    with open(output_html, "w", encoding="utf-8") as fh:
        for fig in charts:
            fh.write(fig.to_html(full_html=False, include_plotlyjs='cdn'))

