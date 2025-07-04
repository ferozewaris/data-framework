"""Generate configuration files using LLM assistance."""

from __future__ import annotations

from typing import Any, Dict
import os
import requests
import yaml
import pandas as pd
from utils import detect_schema, write_yaml


SYSTEM_PROMPT = (
    "You are a data engineer assistant. Generate YAML configs for cleaning, "
    "aggregations and dashboards based on the provided schema and user request."
)

# Hugging Face model used for inference
HF_MODEL = os.environ.get("HF_MODEL", "google/flan-t5-large")
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")


def _query_huggingface(prompt: str) -> str:
    """Send a text generation request to the Hugging Face inference API."""
    headers = {"Authorization": f"Bearer {HF_API_TOKEN}"} if HF_API_TOKEN else {}
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    payload = {"inputs": prompt, "options": {"wait_for_model": True}}
    resp = requests.post(url, headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    data = resp.json()
    if isinstance(data, list) and data and "generated_text" in data[0]:
        return data[0]["generated_text"]
    if isinstance(data, dict) and "generated_text" in data:
        return data["generated_text"]
    # Fall back to string conversion
    return str(data)


def generate_config(data_path: str, user_prompt: str, output_path: str = "config.yaml") -> Dict[str, Any]:
    """Inspect data and generate configuration using a Hugging Face model."""
    schema = detect_schema(data_path)
    prompt = (
        f"{SYSTEM_PROMPT}\nSchema: {schema}\nUser request: {user_prompt}\n"
        "Return YAML with sections: cleaning, aggregations, dashboard."
    )

    content = _query_huggingface(prompt)
    try:
        config = yaml.safe_load(content)
    except Exception:
        config = {}
    write_yaml(config, output_path)
    return config

