import json
from pathlib import Path

import os
import psycopg2


INPUT_FILE = Path("data/processed/hcpcs_transformed.json")


DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "database": os.getenv("DB_NAME", "hcpcs_db"),
    "user": os.getenv("DB_USER", "hcpcs_user"),
    "password": os.getenv("DB_PASSWORD", "hcpcs_password"),
}


def validate_json(records):
    errors = []

    if not records:
        errors.append("No records found in input file.")

    for record in records:
        if not record.get("hcpcs_code"):
            errors.append("Missing hcpcs_code.")

        if not record.get("group_code"):
            errors.append(
                f"Missing group_code for {record.get('hcpcs_code')}."
            )

        if not record.get("long_description"):
            errors.append(
                f"Missing long_description for {record.get('hcpcs_code')}."
            )

        desc_hash = record.get("desc_hash")

        if not desc_hash:
            errors.append(
                f"Missing desc_hash for {record.get('hcpcs_code')}."
            )
        elif len(desc_hash) != 32:
            errors.append(
                f"Invalid desc_hash for {record.get('hcpcs_code')}."
            )

    codes = [
        record["hcpcs_code"]
        for record in records
        if record.get("hcpcs_code")
    ]

    if len(codes) != len(set(codes)):
        errors.append("Duplicate HCPCS codes found.")

    return errors


def validate_database():
    errors = []

    connection = psycopg2.connect(
        **DB_CONFIG
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM hcpcs_codes
        WHERE hcpcs_code IS NULL
        """
    )

    null_codes = cursor.fetchone()[0]

    if null_codes > 0:
        errors.append(
            f"{null_codes} records have NULL hcpcs_code."
        )

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM hcpcs_codes
        WHERE long_description IS NULL
        """
    )

    null_descriptions = cursor.fetchone()[0]

    if null_descriptions > 0:
        errors.append(
            f"{null_descriptions} records have NULL descriptions."
        )

    cursor.execute(
        """
        SELECT hcpcs_code, COUNT(*)
        FROM hcpcs_codes
        WHERE is_current = TRUE
        GROUP BY hcpcs_code
        HAVING COUNT(*) > 1
        """
    )

    duplicate_current = cursor.fetchall()

    if duplicate_current:
        errors.append(
            "Multiple current records found for HCPCS codes."
        )

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM hcpcs_codes
        WHERE desc_hash IS NULL
           OR LENGTH(desc_hash) != 32
        """
    )

    invalid_hashes = cursor.fetchone()[0]

    if invalid_hashes > 0:
        errors.append(
            f"{invalid_hashes} records have invalid desc_hash."
        )

    cursor.close()
    connection.close()

    return errors


def update_validation_metrics(dq_failures):
    connection = psycopg2.connect(
        **DB_CONFIG
    )

    cursor = connection.cursor()

    if dq_failures == 0:
        cursor.execute(
            """
            INSERT INTO pipeline_metrics (
                pipeline_name,
                dq_failures,
                last_success_ts
            )
            VALUES (
                %s,
                %s,
                CURRENT_TIMESTAMP
            )
            ON CONFLICT (pipeline_name)
            DO UPDATE SET
                dq_failures = EXCLUDED.dq_failures,
                last_success_ts = EXCLUDED.last_success_ts
            """,
            ("hcpcs_pipeline", 0)
        )
    else:
        cursor.execute(
            """
            INSERT INTO pipeline_metrics (
                pipeline_name,
                dq_failures
            )
            VALUES (
                %s,
                %s
            )
            ON CONFLICT (pipeline_name)
            DO UPDATE SET
                dq_failures = EXCLUDED.dq_failures
            """,
            ("hcpcs_pipeline", dq_failures)
        )

    connection.commit()
    cursor.close()
    connection.close()


def main():
    with INPUT_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        records = json.load(file)

    json_errors = validate_json(records)
    database_errors = validate_database()

    errors = json_errors + database_errors

    print("HCPCS Data Quality Report")
    print("=========================")
    print(f"Input records: {len(records)}")
    print(f"Validation errors: {len(errors)}")

    if errors:
        print()
        print("FAILED")
        print("-------------------------")

        for error in errors:
            print(f"- {error}")

        update_validation_metrics(len(errors))
        raise SystemExit(1)

    print()
    print("PASSED")
    print("All data quality checks passed.")

    update_validation_metrics(0)


if __name__ == "__main__":
    main()
