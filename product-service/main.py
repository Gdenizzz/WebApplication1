from fastapi import FastAPI
from routes import router as product_router
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Product Service")
app.include_router(product_router)
Instrumentator().instrument(app).expose(app)

@app.get("/")
def root():
    return {"message": "Product Service is running"}



