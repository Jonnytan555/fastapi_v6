from dotenv import load_dotenv
import os


def get_db_url() -> str:
    """
    Server version:
      - Always load /home/jedwards1/app/.env
      - Prefer DATABASE_URL if set
      - Otherwise build from DATABASE_* parts
      - Do NOT use HEROKU_DB_URL here
    """

    # 🔹 Always load the env file from the app root on this server
    load_dotenv("/home/jedwards1/app/.env")

    # Optional: explicit debug so you know this version is being used
    print("⚙️ get_db_url(): loading /home/jedwards1/app/.env")

    # 1️⃣ Optional full URL override (e.g. if you ever set DATABASE_URL)
    url = os.getenv("DATABASE_URL")

    # 2️⃣ Fallback: build from parts in .env
    if not url:
        db_user = os.getenv("DATABASE_USER", "postgres")
        db_pass = os.getenv("DATABASE_PASSWORD", "")
        db_host = os.getenv("DATABASE_HOSTNAME", "localhost")
        db_port = os.getenv("DATABASE_PORT", "5432")
        db_name = os.getenv("DATABASE_NAME", "fastapi-prod")

        url = f"postgresql+psycopg2://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

    # 3️⃣ Normalize postgres scheme
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    elif url.startswith("postgresql://") and "+psycopg2" not in url:
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)

    # For local/server DB we don't force sslmode unless you want it:
    # sslmode = os.getenv("DATABASE_SSLMODE")
    # if sslmode and "sslmode=" not in url:
    #     sep = "&" if "?" in url else "?"
    #     url = f"{url}{sep}sslmode={sslmode}"

    print("🔗 get_db_url returning:", url)
    return url
