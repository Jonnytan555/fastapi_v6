import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------
# Force test environment
# ---------------------------------------------------------
os.environ["APP_ENV"] = "test"
os.environ["ENV_FILE"] = ".env.test"

from app.config import get_settings
settings = get_settings()

from app import models
from app.main import app
from app.database import Base, get_db

# ---------------------------------------------------------
# Build Test Database URL
# ---------------------------------------------------------
TEST_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:"
    f"{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
)

# ---------------------------------------------------------
# Create test engine + sessionmaker
# ---------------------------------------------------------
engine = create_engine(TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# ---------------------------------------------------------
# Make FastAPI use test engine + sessionmaker
# ---------------------------------------------------------
import app.database as db_module
db_module.engine = engine
db_module.SessionLocal = TestingSessionLocal

# ---------------------------------------------------------
# Create all tables ONCE
# ---------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# ---------------------------------------------------------
# PER-TEST TRANSACTION FIXTURE (Option 2: FAST + CLEAN)
# ---------------------------------------------------------
@pytest.fixture()
def db_transaction():
    """
    Creates a new database transaction for each test.
    Rolls back completely afterwards — keeping DB clean.
    """
    connection = engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()  # <--- magic: clean database
        connection.close()

# ---------------------------------------------------------
# Test client using transactional session
# ---------------------------------------------------------
@pytest.fixture()
def client(db_transaction):
    """
    Override FastAPI dependency so each request inside a test
    uses the same transactional session.
    """
    def override_get_db():
        try:
            yield db_transaction
        finally:
            pass  # DO NOT close here

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

# ---------------------------------------------------------
# Fixtures for sample data (users, posts, tokens)
# ---------------------------------------------------------
from app.oauth2 import create_access_token

@pytest.fixture()
def test_user(client):
    data = {"email": "test@example.com", "password": "password123"}
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    return response.json()

@pytest.fixture()
def test_user2(client):
    data = {"email": "test2@example.com", "password": "password1234"}
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    return response.json()

@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture()
def authorised_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}",
    }
    return client

@pytest.fixture()
def test_posts(test_user, test_user2, db_transaction):
    posts = [
        models.Post(title="post title", content="post content", user_id=test_user["id"]),
        models.Post(title="2nd post", content="2nd content", user_id=test_user["id"]),
        models.Post(title="3rd post", content="3rd content", user_id=test_user["id"]),
        models.Post(title="other user post", content="4th content", user_id=test_user2["id"]),
    ]
    db_transaction.add_all(posts)
    db_transaction.commit()
    return db_transaction.query(models.Post).all()

@pytest.fixture()
def test_vote(test_posts, db_transaction, test_user):
    vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    db_transaction.add(vote)
    db_transaction.commit()
