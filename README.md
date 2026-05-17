# IPL Data Pipeline

End-to-end data engineering pipeline built with AWS and Apache Airflow.

## Architecture
Raw Data (Kaggle) → S3 Raw Layer → PySpark Transform → S3 Refined Layer → Airflow Orchestration

## Tech Stack
- AWS S3 — data storage
- Python + boto3 — data ingestion
- Pandas — data transformation
- Apache Airflow — pipeline orchestration
- Databricks — (coming soon)

## Pipeline Steps
1. Upload IPL match data to S3 raw layer
2. Transform and calculate team win statistics
3. Write refined data back to S3
4. Airflow DAG orchestrates steps 1 and 2 daily

## Results
Top IPL teams by wins (2008-2024):
- Mumbai Indians — 144 wins
- Chennai Super Kings — 138 wins
- Kolkata Knight Riders — 131 wins