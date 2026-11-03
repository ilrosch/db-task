import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

APP_CONFIG = {
    "count_records": 1_000_000,
    "res_dir": os.path.join(BASE_DIR, "res"),
    "warn_file": "warn.csv",
    "alarm_file": "alarm.csv",
}
