CREATE TABLE IF NOT EXISTS hcpcs_codes (
    id BIGSERIAL PRIMARY KEY,
    hcpcs_code VARCHAR(50) NOT NULL,
    group_code VARCHAR(10),
    category_name VARCHAR(255),
    long_description TEXT,
    desc_hash CHAR(32),
    effective_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    version INT DEFAULT 1,
    inserted_at TIMESTAMP DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_hcpcs_codes_current
ON hcpcs_codes (hcpcs_code)
WHERE is_current = TRUE;