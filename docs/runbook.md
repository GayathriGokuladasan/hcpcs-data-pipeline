# HCPCS Pipeline Runbook

## 1. Start the Environment

Start PostgreSQL, Airflow, and Metabase:

```bash
docker compose up -d
```

## 2. Check Services

```bash
docker ps
```

Expected services:
- hcpcs-postgres
- hcpcs-airflow
- hcpcs-metabase

## 3. Run the Pipeline Manually

```bash
python src/extract.py
python src/transform.py
python src/load.py
python src/validate.py
```

## 4. Verify Extracted Data

The raw snapshot is stored at:

data/raw/hcpcs_all.json

The processed data is stored at:

data/processed/hcpcs_transformed.json

## 5. Verify Database Records

```bash
docker exec hcpcs-postgres psql -U hcpcs_user -d hcpcs_db -c "SELECT COUNT(*) FROM hcpcs_codes;"
```

The current dataset contains 8,770 HCPCS records.

## 6. Verify Pipeline Metrics

```bash
docker exec hcpcs-postgres psql -U hcpcs_user -d hcpcs_db -c "SELECT * FROM pipeline_metrics;"
```

## 7. Data Quality

Run the validation script:

```bash
python src/validate.py
```

The validation checks missing values, duplicate codes, invalid hashes, and duplicate current records.

## 8. Airflow

The Airflow DAG is named hcpcs_pipeline.

DAG sequence:

Extract -> Transform -> Load -> Validate -> Notify

## 9. Metabase

Metabase provides the HCPCS Data Pipeline Dashboard.

Current dashboard questions:
- Total HCPCS Codes
- HCPCS Codes by Group

## 10. Troubleshooting

### Containers are not running

```bash
docker ps
docker compose logs --tail 100
```

### Airflow task failure

Open the Airflow UI and inspect the failed task logs.

### Database issue

```bash
docker logs hcpcs-postgres
```

## 11. Safe Docker Operations

To stop services without deleting database data:

```bash
docker compose stop
```

Do not use docker compose down -v unless database volumes are intentionally being deleted.
