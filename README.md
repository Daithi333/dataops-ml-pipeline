## DataOps Pipeline for Public Datasets

#### Description

DataOps pipeline designed to ingest, transform, and prepare public datasets (starting with NYC Taxi data) for 
downstream analytics and machine learning. It emphasizes cost-efficient, portable development using Docker, 
dbt for SQL-based transformations, and Python-based ETL for flexible data loading.

#### Key Features

🔁 ETL Engine for loading Parquet datasets into a local Postgres database

🛠️ SQL Transformation Layer using dbt, enabling modular and testable transformations

📦 Containerized Development environment for reproducibility and local-first workflows

🧠 Future-ready for ML — designed to support model training and inference on enriched data

🗃️ Generic, reusable structure for plugging in other public datasets with minimal changes

#### Use Cases

Rapid experimentation with data pipelines

Reproducible data preparation for ML/AI projects

Local data engineering practice without cloud costs

#### Data
- [NY taxi data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

#### Commands

**Verify DB initialised:**
- `docker exec -it dataops_postgres psql -U postgres -d analytics`
- `docker exec -it dataops_postgres psql -U postgres -d airflow`

**Explore analytics table after data insertion:**
```
\dn                                              -- List schemas
\dt nyc_taxi.*                                   -- List tables in the 'nyc_taxi' schema
SELECT COUNT(*) FROM nyc_taxi.yellow_taxi_data;  -- Confirm data is loaded
```

**Start db (independently):**
`docker compose up -d dataops_postgres`

**Load raw data via CLI:**
From the project root and with db container running, run `PYTHONPATH=./src python src/etl.py --dataset nyc_taxi`

**Run dbt (independently):**
`docker compose run --rm dataops_dbt run`

**(Optional) Run dbt tests:**
`docker compose run --rm dataops_dbt test`

**(Optional) Generate dbt docs and serve:**
`docker compose run --rm dataops_dbt docs generate`
`docker compose run --rm dataops_dbt docs serve`

**Inspect dbt entrypoint:**
`docker inspect dataops_dbt --format '{{.Config.Entrypoint}}'`
