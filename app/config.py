from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    APP_NAME: str = Field(default="posts-api")
    APP_ENV: str = Field(default="dev")

    DATABASE_HOSTNAME: str = Field(default="localhost")
    DATABASE_PORT: int = Field(default=5432)
    DATABASE_NAME: str = Field(default="fastapi_v1")
    DATABASE_PASSWORD: str = Field(default="password123")

    SECRET_KEY: str = Field(default="09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = Field(default="HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60)

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()