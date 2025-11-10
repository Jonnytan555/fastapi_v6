import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from fastapi import FastAPI,  Depends
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, get_db
from . import models, config
from . routes import posts, users, vote
from app.database import SessionLocal

print(f"Starting {config.settings.APP_NAME}")

url = os.getenv("HEROKU_DB_URL")

engine = create_engine(url, pool_pre_ping=True) # type: ignore

with engine.connect() as conn:
    result = conn.execute(text("SELECT version();"))
    print(result.scalar())

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(vote.router)

#### ORM TEST Route
@app.get("/sql")
def orm_test(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


@app.get("/")
def get_home():
    return {"mess": "Hello World"}

@app.get("/db-health")
def db_health():
    try:
        with SessionLocal() as db:
            result = db.execute(text("SELECT 1"))
            return {"status": "ok", "result": result.scalar()}
    except Exception as e:
        return {"status": "error", "detail": str(e)}