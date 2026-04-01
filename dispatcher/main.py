from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from auth_client import verify_token
from product_client import get_products, create_product
from order_client import create_order, get_orders
from database import logs_collection
from fastapi import Body
from prometheus_fastapi_instrumentator import Instrumentator
from datetime import datetime

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

def log_request(method: str, path: str, user: dict = None, status: int = 200):
    logs_collection.insert_one({
        "method": method,
        "path": path,
        "user": user.get("email") if user else "anonymous",
        "role": user.get("role") if user else None,
        "status": status,
        "timestamp": datetime.utcnow()
    })

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
        log_request("GET", "/protected", status=401)
        raise HTTPException(status_code=401, detail="Unauthorized")
    log_request("GET", "/protected", user=user)
    return {"message": "Access granted", "user": user}

@app.get("/products")
def dispatcher_products(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        log_request("GET", "/products", status=401)
        raise HTTPException(status_code=401, detail="Unauthorized")
    products = get_products()
    log_request("GET", "/products", user=user)
    return {"user": user, "products": products}

@app.post("/products")
def dispatcher_create_product(
    payload: dict = Body(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        log_request("POST", "/products", status=401)
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user.get("role") != "admin":
        log_request("POST", "/products", user=user, status=403)
        raise HTTPException(status_code=403, detail="Bu islem icin admin yetkisi gerekiyor")
    result = create_product(payload)
    log_request("POST", "/products", user=user)
    return result

@app.post("/orders")
def dispatcher_create_order(
    payload: dict = Body(...),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        log_request("POST", "/orders", status=401)
        raise HTTPException(status_code=401, detail="Unauthorized")
    payload["user_id"] = user["email"]
    result = create_order(payload)
    log_request("POST", "/orders", user=user)
    return result

@app.get("/orders")
def dispatcher_get_orders(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        log_request("GET", "/orders", status=401)
        raise HTTPException(status_code=401, detail="Unauthorized")
    orders = get_orders(user["email"])
    log_request("GET", "/orders", user=user)
    return {"user": user, "orders": orders}

@app.get("/logs")
def get_logs(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    if user.get("role") != "admin":
        raise HTTPException(status_code=403, detail="Bu islem icin admin yetkisi gerekiyor")
    logs = []
    for log in logs_collection.find().sort("timestamp", -1).limit(100):
        log["_id"] = str(log["_id"])
        log["timestamp"] = log["timestamp"].isoformat()
        logs.append(log)
    return logs


@app.post("/auth/register")
def dispatcher_register(payload: dict = Body(...)):
    try:
        response = __import__('requests').post(
            "http://auth-service:8000/auth/register",
            json=payload
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/auth/login")
def dispatcher_login(payload: dict = Body(...)):
    try:
        response = __import__('requests').post(
            "http://auth-service:8000/auth/login",
            json=payload
        )
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))