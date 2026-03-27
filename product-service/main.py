from fastapi import FastAPI
from routes import router as product_router

app = FastAPI(title="Product Service")

app.include_router(product_router)


@app.get("/")
def root():
    return {"message": "Product Service is running"}