from fastapi import APIRouter, HTTPException,Depends
from models import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, MeResponse, VerifyResponse
from database import users_collection
import bcrypt
from jose import jwt,JWTError
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
security = HTTPBearer()

router = APIRouter(prefix="/auth", tags=["Auth"])

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


@router.post("/register", response_model=RegisterResponse)
def register_user(payload: RegisterRequest):
    email = str(payload.email)
    full_name = str(payload.full_name)
    role = str(payload.role)

    existing_user = users_collection.find_one({"email": email})

    if existing_user:
        raise HTTPException(status_code=400, detail="Bu email zaten kayıtlı")

    hashed_password = bcrypt.hashpw(
        payload.password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    new_user = {
        "email": email,
        "password_hash": hashed_password,
        "full_name": full_name,
        "role": role,
        "is_active": True,
        "created_at": "2026-03-14T00:00:00Z",
        "updated_at": "2026-03-14T00:00:00Z"
    }

    result = users_collection.insert_one(new_user)

    return RegisterResponse(
        message="Kullanıcı başarıyla oluşturuldu",
        user_id=str(result.inserted_id),
        email=email,
        role=role
    )


@router.post("/login", response_model=LoginResponse)
def login_user(payload: LoginRequest):
    email = str(payload.email)

    user = users_collection.find_one({"email": email})

    if not user:
        raise HTTPException(status_code=401, detail="Email veya şifre hatalı")

    if not bcrypt.checkpw(
        payload.password.encode("utf-8"),
        user["password_hash"].encode("utf-8")
    ):
        raise HTTPException(status_code=401, detail="Email veya şifre hatalı")

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    token_data = {
        "sub": str(user["_id"]),
        "email": user["email"],
        "role": user["role"],
        "exp": expire
    }

    access_token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    return LoginResponse(
        message="Giriş başarılı",
        access_token=access_token,
        token_type="bearer"
    )


security = HTTPBearer()


@router.get("/me", response_model=MeResponse)
def get_me(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return MeResponse(
            user_id=payload["sub"],
            email=payload["email"],
            role=payload["role"]
        )

    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz veya süresi dolmuş token")


@router.post("/verify", response_model=VerifyResponse)
def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        return VerifyResponse(
            valid=True,
            user_id=payload["sub"],
            email=payload["email"],
            role=payload["role"]
        )

    except JWTError:
        raise HTTPException(status_code=401, detail="Geçersiz token")