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

**Start the db:**
As dbt typically gets run ephemerally, start the db container on its own with `docker compose up -d data_postgres`

**Load raw data into Postgres:**
From the project root, run `PYTHONPATH=. python datasets/nyc_taxi/etl/load_data.py`

**Run dbt:**
`docker compose run --rm dbt_nyc_taxi run`

**(Optional) Run dbt tests:**
`docker compose run --rm dbt_nyc_taxi test`

**(Optional) Generate docs and serve:**
`docker compose run --rm dbt_nyc_taxi docs generate`
`docker compose run --rm dbt_nyc_taxi docs serve`
