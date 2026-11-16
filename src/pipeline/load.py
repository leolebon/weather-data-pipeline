import logging
import psycopg

logger = logging.getLogger(__name__)
CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS weather_observations (
    id BIGSERIAL PRIMARY KEY,
    city TEXT NOT NULL,
    observed_at TIMESTAMPTZ NOT NULL,
    temperature_2m DOUBLE PRECISION NOT NULL,
    relative_humidity_2m DOUBLE PRECISION NOT NULL,
    precipitation DOUBLE PRECISION NOT NULL,
    wind_speed_10m DOUBLE PRECISION NOT NULL,
    loaded_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (city, observed_at)
);
'''
UPSERT = '''
INSERT INTO weather_observations
(city, observed_at, temperature_2m, relative_humidity_2m, precipitation, wind_speed_10m)
VALUES (%(city)s, %(observed_at)s, %(temperature_2m)s, %(relative_humidity_2m)s, %(precipitation)s, %(wind_speed_10m)s)
ON CONFLICT (city, observed_at) DO UPDATE SET
temperature_2m=EXCLUDED.temperature_2m,
relative_humidity_2m=EXCLUDED.relative_humidity_2m,
precipitation=EXCLUDED.precipitation,
wind_speed_10m=EXCLUDED.wind_speed_10m,
loaded_at=NOW();
'''

def load_records(records, db_config):
    if not records:
        return 0
    with psycopg.connect(**db_config) as conn:
        with conn.cursor() as cur:
            cur.execute(CREATE_TABLE)
            cur.executemany(UPSERT, records)
    logger.info("Upserted %d records", len(records))
    return len(records)
