from unittest.mock import MagicMock

from src.load import update_rows_loaded


def test_update_rows_loaded():
    cursor = MagicMock()

    update_rows_loaded(cursor, 8770)

    cursor.execute.assert_called_once()

    sql, parameters = cursor.execute.call_args[0]

    assert "INSERT INTO pipeline_metrics" in sql
    assert "rows_loaded" in sql
    assert parameters == ("hcpcs_pipeline", 8770)
