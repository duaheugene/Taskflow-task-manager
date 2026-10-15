"""Basic API integration tests using an isolated SQLite test database."""
import os
import tempfile

# Ensure the test database is selected before importing the application.
_fd, _db_path = tempfile.mkstemp(suffix=".db")
os.close(_fd)
os.environ["DATABASE_URL"] = f"sqlite:///{_db_path}"
os.environ["SECRET_KEY"] = "test-secret-key-not-for-production"

from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def register(email="one@example.com", name="Test User"):
    response = client.post("/api/auth/register", json={"name": name, "email": email, "password": "password123"})
    assert response.status_code == 201, response.text
    return response.json()["access_token"]


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_register_login_and_duplicate_email():
    token = register()
    assert token
    duplicate = client.post("/api/auth/register", json={"name": "Another User", "email": "one@example.com", "password": "password123"})
    assert duplicate.status_code == 409
    login = client.post("/api/auth/login", json={"email": "one@example.com", "password": "password123"})
    assert login.status_code == 200
    assert login.json()["user"]["email"] == "one@example.com"


def test_task_crud_and_validation():
    token = register()
    headers = {"Authorization": f"Bearer {token}"}
    created = client.post("/api/tasks", headers=headers, json={"title": "Learn FastAPI", "description": "CRUD project", "priority": "high"})
    assert created.status_code == 201
    task = created.json()
    task_id = task["id"]
    assert task["status"] == "pending"

    listing = client.get("/api/tasks", headers=headers)
    assert listing.status_code == 200 and len(listing.json()) == 1

    updated = client.patch(f"/api/tasks/{task_id}", headers=headers, json={"status": "completed"})
    assert updated.status_code == 200
    assert updated.json()["completed"] is True

    deleted = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert deleted.status_code == 204
    missing = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert missing.status_code == 404


def test_users_cannot_access_each_others_tasks():
    token_one = register("one@example.com", "User One")
    token_two = register("two@example.com", "User Two")
    task = client.post("/api/tasks", headers={"Authorization": f"Bearer {token_one}"}, json={"title": "Private task"}).json()
    other_headers = {"Authorization": f"Bearer {token_two}"}
    assert client.get(f"/api/tasks/{task['id']}", headers=other_headers).status_code == 404
    assert client.patch(f"/api/tasks/{task['id']}", headers=other_headers, json={"title": "Stolen"}).status_code == 404
    assert client.delete(f"/api/tasks/{task['id']}", headers=other_headers).status_code == 404


def test_tasks_require_authentication():
    assert client.get("/api/tasks").status_code == 401
    assert client.post("/api/tasks", json={"title": "No auth"}).status_code == 401
