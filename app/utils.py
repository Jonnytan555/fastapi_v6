from dotenv import load_dotenv
import os


def get_db_url() -> str:
    """
    Build database URL depending on environment:
      - If DATABASE_URL or HEROKU_DB_URL exists → use that
      - Else, if .env.prod exists → load it
      - Else, load .env (local dev)
    """

    # 1️⃣ Use DATABASE_URL / HEROKU_DB_URL if defined (Heroku or prod container)
    url = os.getenv("DATABASE_URL") or os.getenv("HEROKU_DB_URL")
    if url:
        # Debug (optional): see what URL we're using
        # print("Using DB URL from env:", url)

        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        if "sslmode" not in url:
            sep = "&" if "?" in url else "?"
            url = f"{url}{sep}sslmode=require"
        return url

    # 2️⃣ If no DATABASE_URL / HEROKU_DB_URL — check for .env.prod or .env
    if os.path.exists(".env.prod"):
        load_dotenv(".env.prod")
    else:
        load_dotenv(".env")

    # Check again in case DATABASE_URL is defined inside .env.prod / .env
    url = os.getenv("DATABASE_URL") or os.getenv("HEROKU_DB_URL")
    if url:
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql+psycopg2://", 1)
        return url

    # 3️⃣ Otherwise, build manually from parts (local)
    db_user = os.getenv("DATABASE_USER", "postgres")
    db_pass = os.getenv("DATABASE_PASSWORD")
    db_host = os.getenv("DATABASE_HOSTNAME", "localhost")
    db_port = os.getenv("DATABASE_PORT", "5432")
    db_name = os.getenv("DATABASE_NAME")

    return f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
