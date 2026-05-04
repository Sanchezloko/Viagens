import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "flights.db"
SEARCHES_PATH = DATA_DIR / "searches.yaml"

SERPAPI_KEY = os.getenv("SERPAPI_KEY", "")

NTFY_TOPIC = os.getenv("NTFY_TOPIC", "")

ALERT_PERCENTILE = float(os.getenv("ALERT_PERCENTILE", "25"))
ALERT_ZSCORE = float(os.getenv("ALERT_ZSCORE", "-1.0"))
MIN_SAMPLES_FOR_ALERT = int(os.getenv("MIN_SAMPLES_FOR_ALERT", "10"))
COOLDOWN_HOURS = int(os.getenv("COOLDOWN_HOURS", "6"))
HISTORY_DAYS = int(os.getenv("HISTORY_DAYS", "90"))
