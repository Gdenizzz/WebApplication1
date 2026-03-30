from fastapi import APIRouter, HTTPException
from database import orders_collection
from models import OrderCreateRequest, OrderResponse, OrderItemResponse
import requests
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["Orders"])

PRODUCT_SERVICE_URL = "http://product-service:8001"


@router.post("/", response_model=OrderResponse)
def create_order(payload: OrderCreateRequest):
    order_items = []
    total_price = 0.0

    response = requests.get(f"{PRODUCT_SERVICE_URL}/products")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Product service erişilemiyor")

    products = response.json()

    for item in payload.items:
        matched_product = next((p for p in products if p["id"] == item.product_id), None)

        if not matched_product:
            raise HTTPException(status_code=404, detail=f"Ürün bulunamadı: {item.product_id}")

        unit_price = matched_product["price"]
        line_total = unit_price * item.quantity

        order_item = {
            "product_id": matched_product["id"],
            "product_name": matched_product["name"],
            "unit_price": unit_price,
            "quantity": item.quantity,
            "line_total": line_total
        }

        order_items.append(order_item)
        total_price += line_total

    new_order = {
        "user_id": payload.user_id,
        "items": order_items,
        "total_price": total_price,
        "status": "created",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = orders_collection.insert_one(new_order)

    return OrderResponse(
        id=str(result.inserted_id),
        user_id=payload.user_id,
        items=[OrderItemResponse(**item) for item in order_items],
        total_price=total_price,
        status="created"
    )


@router.get("/", response_model=list[OrderResponse])
def get_orders():
    orders = []

    for order in orders_collection.find():
        orders.append(OrderResponse(
            id=str(order["_id"]),
            user_id=order["user_id"],
            items=[OrderItemResponse(**item) for item in order["items"]],
            total_price=order["total_price"],
            status=order["status"]
        ))

    return orders




