import json
import os
from pathlib import Path

import psycopg2


INPUT_FILE = Path("data/processed/hcpcs_transformed.json")


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "hcpcs_db"),
    "user": os.getenv("DB_USER", "hcpcs_user"),
    "password": os.getenv("DB_PASSWORD", "hcpcs_password"),
}


def load_data():
    with INPUT_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        records = json.load(file)

    connection = psycopg2.connect(
        **DB_CONFIG
    )

    cursor = connection.cursor()

    inserted_count = 0
    updated_count = 0
    unchanged_count = 0

    for record in records:

        hcpcs_code = record["hcpcs_code"]
        group_code = record["group_code"]
        category_name = record["category_name"]
        long_description = record["long_description"]
        desc_hash = record["desc_hash"]

        cursor.execute(
            """
            SELECT
                id,
                desc_hash,
                version
            FROM hcpcs_codes
            WHERE hcpcs_code = %s
              AND is_current = TRUE
            """,
            (hcpcs_code,)
        )

        existing = cursor.fetchone()

        # New HCPCS code
        if existing is None:

            cursor.execute(
                """
                INSERT INTO hcpcs_codes (
                    hcpcs_code,
                    group_code,
                    category_name,
                    long_description,
                    desc_hash,
                    effective_date,
                    end_date,
                    is_current,
                    version
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    CURRENT_DATE,
                    NULL,
                    TRUE,
                    1
                )
                """,
                (
                    hcpcs_code,
                    group_code,
                    category_name,
                    long_description,
                    desc_hash,
                )
            )

            inserted_count += 1

        else:
            existing_id = existing[0]
            existing_hash = existing[1]
            existing_version = existing[2]

            # No change in description
            if existing_hash == desc_hash:
                unchanged_count += 1
                continue

            # Description changed
            cursor.execute(
                """
                UPDATE hcpcs_codes
                SET
                    end_date = CURRENT_DATE,
                    is_current = FALSE
                WHERE id = %s
                """,
                (existing_id,)
            )

            cursor.execute(
                """
                INSERT INTO hcpcs_codes (
                    hcpcs_code,
                    group_code,
                    category_name,
                    long_description,
                    desc_hash,
                    effective_date,
                    end_date,
                    is_current,
                    version
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    CURRENT_DATE,
                    NULL,
                    TRUE,
                    %s
                )
                """,
                (
                    hcpcs_code,
                    group_code,
                    category_name,
                    long_description,
                    desc_hash,
                    existing_version + 1,
                )
            )

            updated_count += 1

    connection.commit()

    print(f"New records inserted: {inserted_count}")
    print(f"Records versioned: {updated_count}")
    print(f"Records unchanged: {unchanged_count}")

    cursor.close()
    connection.close()


if __name__ == "__main__":
    load_data()