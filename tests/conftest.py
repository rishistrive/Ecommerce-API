import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import (  # Adjust the import based on your project structure
    Base,
    get_db,
)
from app.main import app

# Define a test database URL (change username/password if needed)
TEST_DATABASE_URL = "postgresql://test_user:test_password@localhost/test_db"

# Create a test database engine
engine = create_engine(TEST_DATABASE_URL)

# Create a new session for tests
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """Create a new database session for a test."""
    Base.metadata.create_all(bind=engine)  # Create tables
    session = TestingSessionLocal()
    try:
        yield session  # Provide the session to tests
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)  # Drop tables after test


# Override the database dependency in FastAPI
@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
