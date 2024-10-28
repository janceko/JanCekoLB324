import pytest
from src.app import create_app
from src.models import db, Task

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
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
