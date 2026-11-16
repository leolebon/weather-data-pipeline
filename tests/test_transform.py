import pytest
from pipeline.transform import transform_payload

@pytest.fixture
def payload():
    return {
        "city": "Lille",
        "hourly": {
            "time": ["2026-11-16T10:00", "2026-11-16T11:00"],
            "temperature_2m": [8.2, 8.7],
            "relative_humidity_2m": [78, 75],
            "precipitation": [0.0, 0.1],
            "wind_speed_10m": [12.5, 13.0],
        },
    }

def test_one_record_per_timestamp(payload):
    rows = transform_payload(payload)
    assert len(rows) == 2
    assert rows[0]["city"] == "Lille"
    assert rows[0]["temperature_2m"] == 8.2

def test_timestamp_is_timezone_aware(payload):
    assert transform_payload(payload)[0]["observed_at"].utcoffset().total_seconds() == 0

def test_misaligned_columns_raise_error(payload):
    payload["hourly"]["temperature_2m"].pop()
    with pytest.raises(ValueError, match="temperature_2m"):
        transform_payload(payload)

def test_missing_values_are_skipped(payload):
    payload["hourly"]["temperature_2m"][0] = None
    rows = transform_payload(payload)
    assert len(rows) == 1
    assert rows[0]["temperature_2m"] == 8.7
