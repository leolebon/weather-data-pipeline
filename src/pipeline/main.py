import logging
from pipeline.config import database_config, load_cities
from pipeline.extract import fetch_weather
from pipeline.load import load_records
from pipeline.transform import transform_payload

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")

def main():
    total = 0
    failures = []
    for city in load_cities():
        try:
            records = transform_payload(fetch_weather(city))
            count = load_records(records, database_config())
            total += count
            logging.info("%s: %d rows loaded", city["city"], count)
        except Exception as exc:
            logging.exception("Failed for %s", city["city"])
            failures.append((city["city"], str(exc)))
    logging.info("Finished: %d rows loaded", total)
    if failures:
        raise RuntimeError(f"Pipeline failed for: {failures}")
