import os
import sys
import pytest

# Füge den src-Pfad zum PYTHONPATH hinzu
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from app import create_app  # Ändere den Import entsprechend deinem Pfad
from models import db, Task  # Ändere den Import entsprechend deinem Pfad

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-Memory-Datenbank für Tests
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.drop_all()

def test_add_task(client):
    response = client.post("/tasks", json={"title": "Test Task"})
    assert response.status_code == 201
    assert response.json["title"] == "Test Task"

def test_get_tasks(client):
    client.post("/tasks", json={"title": "Test Task"})
    response = client.get("/tasks")
    assert response.status_code == 200
    assert len(response.json) > 0

def test_update_task(client):
    client.post("/tasks", json={"title": "Test Task"})
    response = client.put("/tasks/1", json={"completed": True})
    assert response.status_code == 200
    assert response.json["completed"] is True

def test_delete_task(client):
    client.post("/tasks", json={"title": "Test Task"})
    response = client.delete("/tasks/1")
    assert response.status_code == 200
    assert response.json["message"] == "Task deleted successfully"
