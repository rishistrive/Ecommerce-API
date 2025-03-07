from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_product():
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "A product for testing",
            "price": 99.99,
            "stock": 50
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert data["name"] == "Test Product"

def test_create_order():
    # First, create a product for the order
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "A product for testing",
            "price": 99.99,
            "stock": 50
        }
    )
    assert response.status_code == 200
    product = response.json()

    # Now, create an order with that product
    response = client.post(
        "/orders/",
        json={
            "products": [{"product_id": product["id"], "quantity": 1}]
        }
    )
    assert response.status_code == 200
    order = response.json()
    assert "id" in order
    assert order["total_price"] == 99.99

def test_create_order_with_zero_quantity():
    # First, create a product for the order
    response = client.post(
        "/products/",
        json={
            "name": "Test Product",
            "description": "A product for testing",
            "price": 99.99,
            "stock": 50
        }
    )
    assert response.status_code == 200
    product = response.json()

    # Now, try to create an order with zero quantity
    response = client.post(
        "/orders/",
        json={
            "products": [{"product_id": product["id"], "quantity": 0}]
        }
    )
    assert response.status_code == 400  # Expecting a bad request error
    assert "detail" in response.json()

def test_get_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    orders = response.json()
    assert isinstance(orders, list)

def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
