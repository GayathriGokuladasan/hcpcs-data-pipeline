from src.validate import validate_json


def test_validate_json_with_valid_records():
    records = [
        {
            "hcpcs_code": "A0021",
            "group_code": "A",
            "category_name": "Transportation",
            "long_description": "Ambulance service",
            "desc_hash": "a" * 32,
        },
        {
            "hcpcs_code": "A0023",
            "group_code": "A",
            "category_name": "Transportation",
            "long_description": "Transportation service",
            "desc_hash": "b" * 32,
        },
    ]

    errors = validate_json(records)

    assert errors == []


def test_validate_json_detects_missing_values():
    records = [
        {
            "hcpcs_code": "",
            "group_code": "A",
            "category_name": "Transportation",
            "long_description": "",
            "desc_hash": "",
        }
    ]

    errors = validate_json(records)

    assert "Missing hcpcs_code." in errors
    assert "Missing long_description for ." in errors
    assert "Missing desc_hash for ." in errors


def test_validate_json_detects_invalid_hash():
    records = [
        {
            "hcpcs_code": "A0021",
            "group_code": "A",
            "category_name": "Transportation",
            "long_description": "Ambulance service",
            "desc_hash": "abc123",
        }
    ]

    errors = validate_json(records)

    assert len(errors) == 1
    assert "Invalid desc_hash for A0021." in errors


def test_validate_json_detects_duplicate_codes():
    records = [
        {
            "hcpcs_code": "A0021",
            "group_code": "A",
            "category_name": "Transportation",
            "long_description": "Ambulance service",
            "desc_hash": "a" * 32,
        },
        {
            "hcpcs_code": "A0021",
            "group_code": "A",
            "category_name": "Transportation",
            "long_description": "Another service",
            "desc_hash": "b" * 32,
        },
    ]

    errors = validate_json(records)

    assert "Duplicate HCPCS codes found." in errors
