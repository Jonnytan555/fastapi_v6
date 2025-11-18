from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = Field(default="posts-api")
    APP_ENV: str = Field(default="dev")

    DATABASE_HOSTNAME: str = Field(default="localhost")
    DATABASE_PORT: int = Field(default=5432)
    DATABASE_NAME: str = Field(default="fastapi_v1")
    DATABASE_PASSWORD: str = Field(default="password123")
    HEROKU_DB_URL: str = Field(default="postgres://u1l78angvcvih8:pce0636f6843a78f9ac64dcaab3a16c54470cb656e95600cf96fa3ee7dae45d3a@c57oa7dm3pc281.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d7fs6q0jp56jd6")
  
    SECRET_KEY: str = Field(default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    class Config:
        env_file = str(Path(__file__).resolve().parent.parent / ".env")
        env_file_encoding = "utf-8"

settings = Settings()