# Gen-AI Data Pipeline Framework

This project demonstrates a modular data pipeline that uses generative AI to build configurations for cleaning, aggregation and dashboard generation.

## Usage

```bash
python main.py path/to/data.csv "Show customer churn trends" --provider openai
```

The pipeline will:

1. Inspect the dataset and generate a YAML config with the help of an LLM.
2. Ingest the dataset.
3. Clean and normalize the data.
4. Aggregate according to the generated rules.
5. Produce an HTML dashboard with charts based on the user intent.

## Extending

- New data sources can be added by extending `ingestion.ingest`.
- Additional chart types can be implemented in `dashboard.generate_charts`.
- Different LLM providers can be plugged into `llm_config_generator.py` and selected at runtime with the `--provider` option.

## Configuration Template

The prompt sent to the LLM includes a YAML example so the model understands the
expected structure:

```yaml
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
```

## Environment Variables

Set the following variables to provide credentials and model IDs:

- `HF_MODEL` / `HF_API_TOKEN` for Hugging Face
- `OPENAI_MODEL` / `OPENAI_API_KEY` for OpenAI
- `GEMINI_MODEL` / `GOOGLE_API_KEY` for Google Gemini
- `META_MODEL_ID` / `REPLICATE_API_TOKEN` for Meta models via Replicate

## How Gen AI Is Used

The `llm_config_generator.generate_config` function sends the schema and user request to the selected LLM provider (Hugging Face, OpenAI, Meta, or Gemini). The generated response includes YAML sections describing cleaning rules, aggregations and dashboard specifications.

