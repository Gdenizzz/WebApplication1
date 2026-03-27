from fastapi import FastAPI
from routes import router as auth_router

app = FastAPI(title="Auth Service")

app.include_router(auth_router)


@app.get("/")
def root():
    return {"message": "Auth Service is running"}


@app.get("/health")
def health():
    return {"status": "ok", "service": "auth-service"}