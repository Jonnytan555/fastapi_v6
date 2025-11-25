# app/utils.py

import os
from pathlib import Path
from dotenv import load_dotenv

# -----------------------------------------------------
# Project root (folder above /app)
# -----------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# -----------------------------------------------------
# Allowed env files
# -----------------------------------------------------
ENV_FILES = {
    "dev": ".env.dev",
    "test": ".env.test",
    "prod": ".env.prod",
}


# -----------------------------------------------------
#  Load environment file path (does NOT load variables)
# -----------------------------------------------------
def load_environment(app_env: str = None) -> Path:
    """
    Return absolute path to the correct .env file based on APP_ENV.
    Does not load the file into environment variables.

    Priority:
       1. Explicit app_env argument
       2. APP_ENV env var
       3. default = "dev"
    """
    env = (app_env or os.getenv("APP_ENV", "dev")).lower()

    if env not in ENV_FILES:
        raise ValueError(f"Unknown environment: {env}")

    env_path = PROJECT_ROOT / ENV_FILES[env]

    if not env_path.exists():
        raise FileNotFoundError(f"Environment file not found: {env_path}")

    return env_path


# -----------------------------------------------------
#  Build DB connection URL
# -----------------------------------------------------
def get_db_url(app_env: str = None) -> str:
    """
    Loads the correct .env file then returns:
        postgresql+psycopg2://user:password@host:port/db
    """
    env_path = load_environment(app_env)
    load_dotenv(env_path)

    user = os.getenv("DATABASE_USER")
    pwd = os.getenv("DATABASE_PASSWORD")
    host = os.getenv("DATABASE_HOSTNAME")
    port = os.getenv("DATABASE_PORT")
    db = os.getenv("DATABASE_NAME")

    return f"postgresql+psycopg2://{user}:{pwd}@{host}:{port}/{db}"
