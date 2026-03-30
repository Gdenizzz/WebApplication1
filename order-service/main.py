from fastapi import FastAPI
from routes import router as order_router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Order Service")
app.include_router(order_router)
Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "Order Service is running"}