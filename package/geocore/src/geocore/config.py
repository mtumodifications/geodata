import os

from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[4]
DATA_DIR = PROJECT_ROOT / "data"

load_dotenv()

# APP_ENV = os.getenv("APP_ENV", "local")

# IS_PRODUCTION = APP_ENV == "production"
# IS_LOCAL = APP_ENV == "local"

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT", "5432"),
    "dbname": os.getenv("DB_NAME", "postgres"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    # "sslmode": "require",
}

DB_URL = (
    f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}"
    f"@{DB_CONFIG['host']}:{DB_CONFIG['port']}"
    f"/{DB_CONFIG['dbname']}"
    # f"?sslmode={DB_CONFIG['sslmode']}"
)
