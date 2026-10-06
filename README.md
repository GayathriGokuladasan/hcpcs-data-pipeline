# HCPCS Data Engineering Pipeline

A complete data engineering pipeline for extracting, transforming, validating, and loading HCPCS data into PostgreSQL.

## Pipeline

1. Extract HCPCS data from the HCPCS website.
2. Store the raw extraction as an immutable JSON snapshot.
3. Transform and normalize the data.
4. Generate an MD5 description hash.
5. Load the data into PostgreSQL.
6. Apply SCD Type 2 when descriptions change.
7. Run data quality validation.
8. Orchestrate the pipeline using Apache Airflow.
9. Track pipeline metrics.
10. Visualize data using Metabase.

## Technology Stack

- Python
- Requests
- BeautifulSoup
- Pandas
- PostgreSQL 18
- psycopg2
- Apache Airflow
- Metabase
- Docker / Docker Compose
- pytest
- GitHub Actions

## Project Structure

```text
airflow/dags/          Airflow DAG
data/raw/              Raw JSON snapshots
data/processed/        Transformed data
database/              PostgreSQL SQL scripts
docs/                  Project documentation
src/                   Pipeline source code
tests/                 Automated tests
Dockerfile             Application container
docker-compose.yml     PostgreSQL, Airflow and Metabase
.env.example           Environment variable template
```

## Running the Pipeline

```bash
docker compose up -d
python src/extract.py
python src/transform.py
python src/load.py
python src/validate.py
```

## Airflow

The Airflow DAG runs Extract -> Transform -> Load -> Validate -> Notify.

## Data Quality

Validation checks include missing values, duplicate HCPCS codes, invalid hashes, and duplicate current database records.

## SCD Type 2

When an HCPCS description changes, the previous version is closed and a new current version is inserted with an incremented version number.

## Monitoring

The pipeline_metrics table tracks rows_loaded, last_success_ts, and dq_failures.

## BI Dashboard

Metabase provides the HCPCS Data Pipeline Dashboard with Total HCPCS Codes and HCPCS Codes by Group.

Current dataset: 8,770 HCPCS records.

## Testing

```bash
pytest -q
```

GitHub Actions runs automated tests and linting.

## Security

Database credentials are supplied through environment variables. The local .env file is excluded from Git. Production deployments should use a dedicated Secrets Manager or Vault.

## Safe Docker Operations

Use docker compose stop to stop services without deleting database data.
Do not use docker compose down -v unless database volumes are intentionally being deleted.
