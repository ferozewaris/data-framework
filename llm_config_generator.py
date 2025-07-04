"""Generate configuration files using LLM assistance."""

from __future__ import annotations

from typing import Any, Dict
import os
import yaml
import pandas as pd
from langchain.llms import HuggingFaceHub
from utils import detect_schema, write_yaml


SYSTEM_PROMPT = (
    "You are a data engineer assistant. Generate YAML configs for cleaning, "
    "aggregations and dashboards based on the provided schema and user request."
)

# Hugging Face model used for inference
HF_MODEL = os.environ.get("HF_MODEL", "google/flan-t5-large")
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")


def _query_huggingface(prompt: str) -> str:
    """Generate text using a Hugging Face model via LangChain."""
    llm = HuggingFaceHub(
        repo_id=HF_MODEL,
        huggingfacehub_api_token=HF_API_TOKEN,
    )
    return llm(prompt)


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

