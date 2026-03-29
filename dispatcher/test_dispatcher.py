import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)

# --- TEMEL TESTLER ---

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "Dispatcher Service is running"

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.json()["service"] == "dispatcher"

# --- YETKİLENDİRME TESTLERİ ---

def test_protected_without_token():
    response = client.get("/protected")
    assert response.status_code == 401

def test_protected_with_invalid_token():
    with patch("main.verify_token", return_value=None):
        response = client.get(
            "/protected",
            headers={"Authorization": "Bearer gecersiz_token"}
        )
    assert response.status_code == 401

def test_protected_with_valid_token():
    fake_user = {"email": "test@test.com"}
    with patch("main.verify_token", return_value=fake_user):
        response = client.get(
            "/protected",
            headers={"Authorization": "Bearer gecerli_token"}
        )
    assert response.status_code == 200
    assert response.json()["user"]["email"] == "test@test.com"

# --- PRODUCTS TESTLERİ ---

def test_products_unauthorized():
    with patch("main.verify_token", return_value=None):
        response = client.get(
            "/products",
            headers={"Authorization": "Bearer gecersiz"}
        )
    assert response.status_code == 401

def test_products_authorized():
    fake_user = {"email": "test@test.com"}
    fake_products = [{"id": "1", "name": "Ürün A"}]
    with patch("main.verify_token", return_value=fake_user), \
         patch("main.get_products", return_value=fake_products):
        response = client.get(
            "/products",
            headers={"Authorization": "Bearer gecerli_token"}
        )
    assert response.status_code == 200
    assert "products" in response.json()

# --- ORDERS TESTLERİ ---

def test_create_order_unauthorized():
    with patch("main.verify_token", return_value=None):
        response = client.post(
            "/orders",
            json={"product_id": "123", "quantity": 2},
            headers={"Authorization": "Bearer gecersiz"}
        )
    assert response.status_code == 401

def test_create_order_authorized():
    fake_user = {"email": "test@test.com"}
    fake_result = {"order_id": "abc", "status": "created"}
    with patch("main.verify_token", return_value=fake_user), \
         patch("main.create_order", return_value=fake_result):
        response = client.post(
            "/orders",
            json={"product_id": "123", "quantity": 2},
            headers={"Authorization": "Bearer gecerli_token"}
        )
    assert response.status_code == 200

def test_get_orders_authorized():
    fake_user = {"email": "test@test.com"}
    fake_orders = [{"order_id": "abc"}]
    with patch("main.verify_token", return_value=fake_user), \
         patch("main.get_orders", return_value=fake_orders):
        response = client.get(
            "/orders",
            headers={"Authorization": "Bearer gecerli_token"}
        )
    assert response.status_code == 200
    assert "orders" in response.json()