import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.main import app
from backend.database import Base, get_db
from backend.utils.security import hash_password
from backend.models.user import User

# Use isolated in-memory or file-based SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test_narrative_studio.db"
test_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    Base.metadata.drop_all(bind=test_engine)
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db_session():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def auth_headers(client, db_session):
    """Provides authenticated test user and headers."""
    email = "testuser@example.com"
    user = db_session.query(User).filter(User.email == email).first()
    if not user:
        user = User(
            username="testuser",
            email=email,
            password_hash=hash_password("password123")
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)

    login_resp = client.post("/api/auth/login", json={
        "email": email,
        "password": "password123"
    })
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
