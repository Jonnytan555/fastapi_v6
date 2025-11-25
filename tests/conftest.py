import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# ---------------------------------------------------------
#  MUST SET ENVIRONMENT *BEFORE ANY APP IMPORTS*
# ---------------------------------------------------------
os.environ["APP_ENV"] = "test"
os.environ["ENV_FILE"] = ".env.test"

print(">>>> APP_ENV:", os.environ["APP_ENV"])
print(">>>> ENV_FILE:", os.environ["ENV_FILE"])

# ---------------------------------------------------------
#  Now import the app (after env is set)
# ---------------------------------------------------------
from app.config import get_settings
settings = get_settings()

from app import models
from app.main import app
from app.database import Base, get_db
from app.oauth2 import create_access_token

# ---------------------------------------------------------
#  Build test database URL
# ---------------------------------------------------------
TEST_DATABASE_URL = (
    f"postgresql+psycopg2://{settings.DATABASE_USER}:"
    f"{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:"
    f"{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
)

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# ---------------------------------------------------------
#  Override DB dependency for test session
# ---------------------------------------------------------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# ---------------------------------------------------------
#  Setup test DB once per session
# ---------------------------------------------------------
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    print(">>>> Dropping & creating test tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    print(">>>> Cleaning up test DB...")
    Base.metadata.drop_all(bind=engine)

# ---------------------------------------------------------
#  Provide TestClient()
# ---------------------------------------------------------
@pytest.fixture()
def client():
    return TestClient(app)

# ---------------------------------------------------------
#  Create test user
# ---------------------------------------------------------
@pytest.fixture()
def test_user(client):
    data = {"email": "test@example.com", "password": "password123"}
    response = client.post("/users/", json=data)
    assert response.status_code == 201
    return response.json()

# ---------------------------------------------------------
#  JWT token for that user
# ---------------------------------------------------------
@pytest.fixture()
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

# ---------------------------------------------------------
#  Authorized client (adds header)
# ---------------------------------------------------------
@pytest.fixture()
def authorised_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}",
    }
    return client

# ---------------------------------------------------------
#  Post fixtures
# ---------------------------------------------------------
@pytest.fixture()
def session():
    """Provides raw DB session (if needed for inserting records)."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def test_posts(test_user, session):
    posts = [
        models.Post(title="post title", content="post content", user_id=test_user["id"]),
        models.Post(title="2nd post", content="2nd content", user_id=test_user["id"]),
        models.Post(title="3rd post", content="3rd content", user_id=test_user["id"]),
    ]
    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()
