from sqlalchemy import create_engine, text
from fastapi import FastAPI,  Depends
from fastapi.middleware.cors import CORSMiddleware

from .routes import posts, users, vote, auth
from app.database import SessionLocal

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

app.include_router(auth.router)

@app.get("/")
def get_home():
    return {"mess": "Welcome to the Posts API!"}

@app.get("/db-health")
def db_health():
    try:
        with SessionLocal() as db:
            result = db.execute(text("SELECT 1"))
            return {"status": "ok", "result": result.scalar()}
    except Exception as e:
        return {"status": "error", "detail": str(e)}