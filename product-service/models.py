from pydantic import BaseModel


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    stock: int
    category: str
    is_active: bool
   
class ProductCreateRequest(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category: str
    is_active: bool = True    