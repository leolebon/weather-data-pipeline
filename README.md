# Weather Data Pipeline

An end-to-end data engineering project: collect hourly weather data from the Open-Meteo API, transform it with Python, and load it into PostgreSQL.

## Architecture
`Open-Meteo API -> Python extraction -> validation/transformation -> PostgreSQL`

## Stack
Python 3.11+, Requests, PostgreSQL, SQL, Docker Compose, pytest.

## Run
1. Start the database: `docker compose up -d db`
2. Create a virtual environment and install the project: `pip install -e .`
3. Copy `.env.example` to `.env` and adjust credentials if needed.
4. Run: `python -m pipeline`
5. Test: `pytest`

The default cities are Lille, Paris, Lyon and Marseille (`config/cities.json`).

## SQL examples
```sql
SELECT DISTINCT ON (city) city, observed_at, temperature_2m
FROM weather_observations ORDER BY city, observed_at DESC;

SELECT city, ROUND(AVG(temperature_2m)::numeric, 2) AS avg_temp
FROM weather_observations GROUP BY city ORDER BY avg_temp DESC;
```

## Engineering choices
- Separate extraction, transformation, loading and configuration modules.
- Validate aligned API columns and skip incomplete observations.
- Timezone-aware timestamps.
- Unique constraint on `(city, observed_at)` and PostgreSQL upsert for idempotent runs.
- Credentials supplied through environment variables.
- Unit tests use mocked API responses; no internet or database is required.

## Limitations and extensions
This version collects hourly forecast values returned by the API, not verified station observations. Future improvements: Airflow/Prefect scheduling, raw JSON/Parquet storage, dbt models, monitoring, CI and a Streamlit dashboard.
