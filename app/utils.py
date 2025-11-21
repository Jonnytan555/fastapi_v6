import os
from dotenv import load_dotenv

def get_env_path() -> str:
    """
    Picks the correct .env file automatically based on:
    - APP_ENV=dev/test/prod
    - OS platform (Windows vs Linux server)
    """
    env = os.getenv("APP_ENV", "dev").lower()

    # Linux server path
    if os.name == "posix":
        return f"/home/jedwards1/app/.env.{env}"

    # Windows local path
    project_root = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(project_root, f".env.{env}")


def get_db_url() -> str:
    env_path = get_env_path()

    if os.path.exists(env_path):
        print(f"⚙️ Loading env: {env_path}")
        load_dotenv(env_path)
    else:
        raise FileNotFoundError(f"Missing environment file: {env_path}")

    # 1️⃣ Prefer DATABASE_URL (prod)
    url = os.getenv("DATABASE_URL")

    # 2️⃣ If missing, build manually
    if not url:
        user = os.getenv("DATABASE_USER", "postgres")
        passwd = os.getenv("DATABASE_PASSWORD", "")
        host = os.getenv("DATABASE_HOSTNAME", "localhost")
        port = os.getenv("DATABASE_PORT", "5432")
        name = os.getenv("DATABASE_NAME")

        url = f"postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{name}"

    # Normalize schema
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)

    return url
