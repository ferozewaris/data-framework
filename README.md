# Gen-AI Data Pipeline Framework

This project demonstrates a modular data pipeline that uses generative AI to build configurations for cleaning, aggregation and dashboard generation.

## Usage

```bash
python main.py path/to/data.csv "Show customer churn trends over time"
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
- Different LLM providers can be plugged into `llm_config_generator.py`.

## How Gen AI Is Used

The `llm_config_generator.generate_config` function sends the schema and user request to a Hugging Face hosted model. The generated response includes YAML sections describing cleaning rules, aggregations and dashboard specifications.

