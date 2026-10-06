import hashlib

from src.transform import calculate_desc_hash, transform_data


def test_calculate_desc_hash():
    description = "Test description"

    result = calculate_desc_hash(description)

    expected = hashlib.md5(
        description.encode("utf-8")
    ).hexdigest()

    assert result == expected


def test_transform_data():
    records = [
        {
            "hcpcs_code": " A0021 ",
            "group_code": " A ",
            "category_name": " Transportation ",
            "long_description": " Test description ",
        }
    ]

    result = transform_data(records)

    assert len(result) == 1

    assert result[0]["hcpcs_code"] == "A0021"
    assert result[0]["group_code"] == "A"
    assert result[0]["category_name"] == "Transportation"
    assert result[0]["long_description"] == "Test description"

    expected_hash = hashlib.md5(
        "Test description".encode("utf-8")
    ).hexdigest()

    assert result[0]["desc_hash"] == expected_hash
