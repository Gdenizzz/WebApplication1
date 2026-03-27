from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str
    role: str = "customer"


class RegisterResponse(BaseModel):
    message: str
    user_id: str
    email: EmailStr
    role: str

class LoginRequest(BaseModel):
    email:EmailStr
    password:str


class LoginResponse(BaseModel):
    message:str
    access_token:str
    token_type:str

class MeResponse(BaseModel):
    user_id: str
    email: EmailStr
    role: str    

class VerifyResponse(BaseModel):
    valid: bool
    user_id: str
    email: EmailStr
    role: str
    
    