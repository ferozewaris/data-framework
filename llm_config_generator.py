"""Generate configuration files using LLM assistance."""

from __future__ import annotations

from typing import Any, Dict
import os
import yaml
import pandas as pd
from langchain.llms import HuggingFaceHub
from langchain.chat_models import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import Replicate
from utils import detect_schema, write_yaml


SYSTEM_PROMPT = (
    "You are a data engineer assistant. Generate YAML configs for cleaning, "
    "aggregations and dashboards based on the provided schema and user request."
)

# Example YAML structure for the configuration
YAML_TEMPLATE = """
cleaning:
  deduplicate: true
  column_a:
    fillna: 0
    astype: int
aggregations:
  - name: sample_agg
    group_by: [column_b]
    metrics:
      - column: column_a
        agg: sum
dashboard:
  - type: bar
    x: column_b
    y: column_a_sum
    title: "Sample Bar Chart"
"""

# Hugging Face model used for inference
HF_MODEL = os.environ.get("HF_MODEL", "google/flan-t5-large")
HF_API_TOKEN = os.environ.get("HF_API_TOKEN")

# OpenAI model and API key
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

# Gemini model
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-pro")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Meta/Replicate model
META_MODEL_ID = os.environ.get("META_MODEL_ID", "meta/llama-13b")
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")


def _query_huggingface(prompt: str) -> str:
    """Generate text using a Hugging Face model via LangChain."""
    llm = HuggingFaceHub(
        repo_id=HF_MODEL,
        huggingfacehub_api_token=HF_API_TOKEN,
    )
    return llm(prompt)


def _query_openai(prompt: str) -> str:
    """Generate text using an OpenAI model via LangChain."""
    llm = ChatOpenAI(model_name=OPENAI_MODEL, openai_api_key=OPENAI_API_KEY)
    return llm.predict(prompt)


def _query_gemini(prompt: str) -> str:
    """Generate text using Google's Gemini model."""
    llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=GOOGLE_API_KEY)
    return llm.invoke(prompt)


def _query_meta(prompt: str) -> str:
    """Generate text using a Meta LLM via Replicate."""
    llm = Replicate(
        model=META_MODEL_ID,
        token=REPLICATE_API_TOKEN,
    )
    return llm(prompt)


_QUERY_FUNCS = {
    "huggingface": _query_huggingface,
    "openai": _query_openai,
    "gemini": _query_gemini,
    "meta": _query_meta,
}


def _query_model(prompt: str, provider: str) -> str:
    """Dispatch prompt to the chosen LLM provider."""
    func = _QUERY_FUNCS.get(provider.lower())
    if not func:
        raise ValueError(f"Unsupported LLM provider: {provider}")
    return func(prompt)


def generate_config(
    data_path: str,
    user_prompt: str,
    output_path: str = "config.yaml",
    provider: str = "huggingface",
) -> Dict[str, Any]:
    """Inspect data and generate configuration using the specified LLM provider."""
    schema = detect_schema(data_path)
    prompt = (
        f"{SYSTEM_PROMPT}\n"
        f"Schema: {schema}\n"
        "Use the following YAML format:\n"
        f"{YAML_TEMPLATE}\n"
        f"User request: {user_prompt}\n"
        "Return YAML with sections: cleaning, aggregations, dashboard."
    )

    content = _query_model(prompt, provider)
    try:
        config = yaml.safe_load(content)
    except Exception:
        config = {}
    write_yaml(config, output_path)
    return config

