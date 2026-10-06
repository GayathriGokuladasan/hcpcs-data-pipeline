import hashlib
import json
from pathlib import Path


INPUT_FILE = Path("data/raw/hcpcs_all.json")
OUTPUT_FILE = Path("data/processed/hcpcs_transformed.json")


def calculate_desc_hash(description):
    return hashlib.md5(
        description.encode("utf-8")
    ).hexdigest()


def transform_data(records):
    transformed_records = []

    for record in records:
        hcpcs_code = record["hcpcs_code"].strip()
        group_code = record["group_code"].strip()
        category_name = record["category_name"].strip()
        long_description = record["long_description"].strip()

        desc_hash = calculate_desc_hash(
            long_description
        )

        transformed_records.append(
            {
                "hcpcs_code": hcpcs_code,
                "group_code": group_code,
                "category_name": category_name,
                "long_description": long_description,
                "desc_hash": desc_hash,
            }
        )

    return transformed_records


def main():
    with INPUT_FILE.open(
        "r",
        encoding="utf-8"
    ) as file:
        records = json.load(file)

    transformed_records = transform_data(
        records
    )

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with OUTPUT_FILE.open(
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(
            transformed_records,
            file,
            indent=2,
            ensure_ascii=False
        )

    print(
        f"Transformed {len(transformed_records)} records."
    )

    print(
        f"Processed data saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()
