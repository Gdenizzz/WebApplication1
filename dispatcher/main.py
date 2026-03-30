from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth_client import verify_token
from product_client import get_products
from order_client import create_order
from order_client import get_orders
from fastapi import Body
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Dispatcher Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Instrumentator().instrument(app).expose(app)
security = HTTPBearer()

@app.get("/")
def root():
    return {"message": "Dispatcher Service is running"}

@app.get("/health")
def health():
    return {"status": "ok", "service": "dispatcher"}

@app.get("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return {
        "message": "Access granted",
        "user": user
    }

@app.get("/products")
def dispatcher_products(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    products = get_products()
    return {
        "user": user,
        "products": products
    }

@app.post("/orders")
def dispatcher_create_order(
    payload: dict = Body(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload["user_id"] = user["email"]
    result = create_order(payload)
    return result

@app.get("/orders")
def dispatcher_get_orders(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    orders = get_orders()
    return {
        "user": user,
        "orders": orders
    }