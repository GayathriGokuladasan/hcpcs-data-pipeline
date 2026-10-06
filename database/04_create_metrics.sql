CREATE TABLE IF NOT EXISTS pipeline_metrics (
    pipeline_name VARCHAR(100) PRIMARY KEY,
    rows_loaded BIGINT DEFAULT 0,
    last_success_ts TIMESTAMP,
    dq_failures INT DEFAULT 0
);
