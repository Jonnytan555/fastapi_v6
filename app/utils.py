from dotenv import load_dotenv
import os


def get_db_url() -> str:
    """
    Build database URL depending on environment:
      - If DATABASE_URL or HEROKU_DB_URL exists → use that
      - Else, if .env.prod exists → load it
      - Else, load .env (local dev)
      - Always normalize to postgresql+psycopg2 for consistency.
    """

    # 1️⃣ Use DATABASE_URL / HEROKU_DB_URL if defined (Heroku or prod)
    url = os.getenv("DATABASE_URL") or os.getenv("HEROKU_DB_URL")

    # 2️⃣ If not set, load env files (local only)
    if not url:
        if os.path.exists(".env.prod"):
            load_dotenv(".env.prod")
        else:
            load_dotenv(".env")

        url = os.getenv("DATABASE_URL") or os.getenv("HEROKU_DB_URL")

    # 3️⃣ Still nothing? Build from parts (local dev fallback)
    if not url:
        db_user = os.getenv("DATABASE_USER", "postgres")
        db_pass = os.getenv("DATABASE_PASSWORD")
        db_host = os.getenv("DATABASE_HOSTNAME", "localhost")
        db_port = os.getenv("DATABASE_PORT", "5432")
        db_name = os.getenv("DATABASE_NAME")
        url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # 4️⃣ Normalize schemes:
    # - Heroku gives postgres:// → we want postgresql+psycopg2://
    # - If it's already postgresql://, also force +psycopg2
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif url.startswith("postgresql://") and "+psycopg" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)

    # 5️⃣ Ensure sslmode=require in production-ish scenarios
    if "sslmode" not in url:
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}sslmode=require"

    # Debug: you can keep this for now, then remove
    print("🔗 get_db_url returning:", url)

    return url