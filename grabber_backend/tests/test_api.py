from fastapi.testclient import TestClient
import pytest
from grabber_backend.api.app import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_create_order():
    order = {
        "user": "jonasb",
        "order_items": [{"product_id": "12", "quantity": 3, "price": "12.00"}],
        "payment_method": "pix",
        "total_price": "36.00",
    }
    response = client.post("/orders/", json=order)
    assert response.status_code == 200
    assert response.json() == {"status": "Order sent"}
