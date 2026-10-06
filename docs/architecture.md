# HCPCS Data Pipeline Architecture

## Overview
The HCPCS data pipeline extracts HCPCS data, transforms it, validates it, loads it into PostgreSQL, and exposes the data through Metabase.

## Architecture Flow

HCPCS Website -> Extract -> Raw JSON -> Transform -> PostgreSQL -> Validate -> Metrics -> Metabase

## Components

### Extraction
Python Requests and BeautifulSoup extract HCPCS codes, group codes, category names, and descriptions.

### Transformation
The transformation stage normalizes fields and generates an MD5 description hash.

### PostgreSQL Warehouse
PostgreSQL stores the transformed data in the hcpcs_codes table.

### SCD Type 2
Description changes create a new current version while preserving the previous version as historical data.

### Data Quality
Validation checks missing values, duplicate HCPCS codes, invalid hashes, and duplicate current records.

### Airflow
Airflow orchestrates Extract -> Transform -> Load -> Validate -> Notify.

### Monitoring
The pipeline_metrics table tracks rows_loaded, last_success_ts, and dq_failures.

### BI
Metabase connects to PostgreSQL and provides the HCPCS Data Pipeline Dashboard.
