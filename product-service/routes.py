from fastapi import APIRouter
from database import products_collection
from models import ProductResponse
from bson import ObjectId

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductResponse])
def get_products():
    products = []

    for product in products_collection.find():
        products.append(ProductResponse(
            id=str(product["_id"]),
            name=product.get("name", ""),
            description=product.get("description", ""),
            price=product.get("price", 0),
            stock=product.get("stock", 0),
            category=product.get("category", ""),
            is_active=product.get("is_active", True)
        ))

    return products



from models import ProductCreateRequest
from datetime import datetime


@router.post("/")
def create_product(payload: ProductCreateRequest):

    new_product = {
        "name": payload.name,
        "description": payload.description,
        "price": payload.price,
        "stock": payload.stock,
        "category": payload.category,
        "is_active": payload.is_active,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }

    result = products_collection.insert_one(new_product)

    return {
        "message": "Ürün eklendi",
        "product_id": str(result.inserted_id)
    }



# Stok güncelleme endpoint'i order-service tarafından çağrılacak
@router.patch("/{product_id}/stock")
def update_stock(product_id: str, payload: dict):
    quantity = payload.get("quantity", 0)
    products_collection.update_one(
        {"_id": ObjectId(product_id)},
        {"$inc": {"stock": -quantity}}
    )
    return {"message": "Stok güncellendi"}

