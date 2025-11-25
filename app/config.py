import os
from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings

from app.utils import load_environment

ROOT = Path(__file__).resolve().parent.parent

print("ENV_FILE:", os.getenv("ENV_FILE"))
print("Using env file:", ROOT / os.getenv("ENV_FILE", ".env.dev"))

class Settings(BaseSettings):
    APP_ENV: str = "dev"

    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_NAME: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ROOT / os.getenv("ENV_FILE", ".env.dev")
        extra = "ignore"

@lru_cache()
def get_settings():
    load_environment()
    return Settings()
