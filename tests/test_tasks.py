import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    db = None
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        if db is not None:
            db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c

def test_create_task(client):
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test Description", "due_date": "2023-11-15T12:00:00", "status": "pending"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

def test_read_tasks(client):
    response = client.get("/tasks/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_read_task(client):
    task = client.post(
        "/tasks/",
        json={"title": "Task to Read", "description": "Test Description", "due_date": "2023-11-15T12:00:00", "status": "pending"}
    )
    task_id = task.json()["id"]
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Task to Read"

def test_update_task(client):
    task = client.post(
        "/tasks/",
        json={"title": "Task to Update", "description": "Test Description", "due_date": "2023-11-15T12:00:00", "status": "pending"}
    )
    task_id = task.json()["id"]
    response = client.put(
        f"/tasks/{task_id}",
        json={"title": "Updated Task", "description": "Updated Description", "due_date": "2023-11-16T12:00:00", "status": "completed"}
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"

def test_delete_task(client):
    task = client.post(
        "/tasks/",
        json={"title": "Task to Delete", "description": "Test Description", "due_date": "2023-11-15T12:00:00", "status": "pending"}
    )
    task_id = task.json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 404