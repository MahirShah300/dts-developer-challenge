import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime


from main import app, get_db
from database import Base, Task

# Test database (in-memory)
TEST_DB_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DB_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture
def test_db_session():
    session = TestingSessionLocal()
    yield session
    session.close()


@pytest.fixture
def client():
    yield TestClient(app)


@pytest.fixture
def insert_test_tasks(test_db_session):
    test_tasks = [
        Task(
            title="Alpha Task",
            description="Test Description for Alpha Task",
            task_status="Pending",
            due_date=datetime.strptime("2025-12-31", "%Y-%m-%d").date(),
        ),
        Task(
            title="Beta Task",
            description="Test Description for Beta Task",
            task_status="Pending",
            due_date=datetime.strptime("2026-12-31", "%Y-%m-%d").date(),
        ),
        Task(
            title="Gamma Cancelled Task",
            description="Test Description Gamma Task",
            task_status="Cancelled",
            due_date=datetime.strptime("2027-12-31", "%Y-%m-%d").date(),
        ),
    ]

    test_db_session.add_all(test_tasks)
    test_db_session.commit()
    yield test_tasks


@pytest.fixture(autouse=True)
def clean_db():
    test_db = TestingSessionLocal()
    test_db.query(Task).delete()
    test_db.commit()
    test_db.close()
