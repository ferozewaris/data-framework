"""Entry point for running the Gen-AI powered pipeline."""

from __future__ import annotations

import argparse
from typing import Any, Dict
import pandas as pd

from llm_config_generator import generate_config
from ingestion import ingest
from cleaning import clean_data
from aggregation import aggregate_data
from dashboard import generate_charts, save_dashboard
from utils import read_yaml
from dotenv import load_dotenv
import os

load_dotenv()
os.environ['HF_API_TOKEN']=os.getenv("HF_API_TOKEN")


def run_pipeline(
    data_source: str,
    prompt: str,
    config_path: str = "config.yaml",
    output_html: str = "dashboard.html",
    provider: str = "huggingface",
) -> None:
    """Run the full pipeline from data ingestion to dashboard creation."""
    config = generate_config(data_source, prompt, output_path=config_path, provider=provider)
    ingest_cfg = {"type": "csv", "path": data_source}
    df = ingest(ingest_cfg)
    df_clean = clean_data(df, config)
    df_gold = aggregate_data(df_clean, config)
    charts = generate_charts(df_gold, config.get("dashboard", []))
    save_dashboard(charts, output_html)


def main() -> None:
    parser = argparse.ArgumentParser(description="Gen-AI data pipeline")
    parser.add_argument("data_source", help="Path to data file or connection string")
    parser.add_argument("prompt", help="Dashboard intent in natural language")
    parser.add_argument(
        "--provider",
        default="huggingface",
        choices=["huggingface", "openai", "meta", "gemini"],
        help="LLM provider to use",
    )
    args = parser.parse_args()
    run_pipeline(args.data_source, args.prompt, provider=args.provider)


if __name__ == "__main__":
    main()

