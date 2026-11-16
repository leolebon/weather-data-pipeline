import json
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
load_dotenv(ROOT / ".env")

def load_cities(path=None):
    with (path or ROOT / "config" / "cities.json").open(encoding="utf-8") as f:
        cities = json.load(f)
    required = {"city", "latitude", "longitude"}
    if not all(required.issubset(city) for city in cities):
        raise ValueError(f"Each city must contain {required}")
    return cities

def database_config():
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "dbname": os.getenv("DB_NAME", "weather"),
        "user": os.getenv("DB_USER", "weather_user"),
        "password": os.getenv("DB_PASSWORD", "change_me"),
    }
