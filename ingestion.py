"""Data ingestion utilities supporting multiple sources."""

from __future__ import annotations

import pandas as pd
import requests
from pymongo import MongoClient
from sqlalchemy import create_engine
from typing import Any, Dict, Optional


def ingest(config: Dict[str, Any]) -> pd.DataFrame:
    """Ingest data based on a configuration dictionary.

    Parameters
    ----------
    config : dict
        Configuration describing the data source. Required keys:
        - type: csv | sql | mongo | api
        - other connection details

    Returns
    -------
    pandas.DataFrame
    """

    source_type = config.get("type")
    if source_type == "csv":
        path = config["path"]
        return pd.read_csv(path)

    if source_type == "sql":
        engine = create_engine(config["connection_string"])
        query = config.get("query", f"SELECT * FROM {config['table']}")
        return pd.read_sql(query, engine)

    if source_type == "mongo":
        client = MongoClient(config["uri"])
        db = client[config["db"]]
        collection = db[config["collection"]]
        records = list(collection.find())
        return pd.DataFrame(records)

    if source_type == "api":
        response = requests.get(config["url"], params=config.get("params"))
        response.raise_for_status()
        data = response.json()
        return pd.DataFrame(data)

    raise ValueError(f"Unsupported source type: {source_type}")

