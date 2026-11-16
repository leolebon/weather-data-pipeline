from datetime import datetime, timezone

FIELDS = ["temperature_2m", "relative_humidity_2m", "precipitation", "wind_speed_10m"]

def transform_payload(payload):
    city = payload["city"]
    hourly = payload.get("hourly", {})
    times = hourly.get("time", [])
    columns = {name: hourly.get(name, []) for name in FIELDS}
    for name, values in columns.items():
        if len(values) != len(times):
            raise ValueError(f"Invalid payload: {name} has {len(values)} values for {len(times)} timestamps")

    records = []
    for i, raw_time in enumerate(times):
        values = {name: columns[name][i] for name in FIELDS}
        if any(value is None for value in values.values()):
            continue
        records.append({
            "city": city,
            "observed_at": datetime.fromisoformat(raw_time).replace(tzinfo=timezone.utc),
            **values,
        })
    return records
