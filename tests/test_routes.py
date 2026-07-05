import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    return app.test_client()


def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == 200


def test_create_item(client):
    new_item = {
        "name": "Test Item",
        "quantity": 5,
        "price": 100
    }
    response = client.post("/items", json=new_item)
    assert response.status_code == 201
    data = response.get_json()
    assert data["name"] == "Test Item"


def test_get_single_item_not_found(client):
    response = client.get("/items/9999")
    assert response.status_code == 404


def test_update_item_not_found(client):
    response = client.put("/items/9999", json={"quantity": 10})
    assert response.status_code == 404


def test_delete_item_not_found(client):
    response = client.delete("/items/9999")
    assert response.status_code == 404