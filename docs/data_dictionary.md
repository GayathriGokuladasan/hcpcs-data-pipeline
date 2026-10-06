# HCPCS Data Dictionary

## hcpcs_codes

| Column | Type | Description |
|---|---|---|
| id | BIGSERIAL | Unique database identifier. |
| hcpcs_code | VARCHAR(50) | HCPCS procedure or service code. |
| group_code | VARCHAR(10) | HCPCS group identifier. |
| category_name | VARCHAR(255) | Category associated with the HCPCS code. |
| long_description | TEXT | Description of the HCPCS code. |
| desc_hash | CHAR(32) | MD5 hash of the description used for change detection. |
| effective_date | DATE | Date from which the record version is effective. |
| end_date | DATE | Date on which the record version becomes inactive. |
| is_current | BOOLEAN | Indicates whether the record is the current version. |
| version | INT | SCD Type 2 version number. |
| inserted_at | TIMESTAMP | Timestamp when the record was inserted. |

## pipeline_metrics

| Column | Type | Description |
|---|---|---|
| pipeline_name | VARCHAR(100) | Name of the pipeline. |
| rows_loaded | BIGINT | Number of records loaded by the pipeline. |
| last_success_ts | TIMESTAMP | Timestamp of the latest successful pipeline run. |
| dq_failures | INT | Number of data quality failures. |
