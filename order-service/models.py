from pydantic import BaseModel
from typing import List


class OrderItemRequest(BaseModel):
    product_id: str
    quantity: int


class OrderCreateRequest(BaseModel):
    user_id: str
    items: List[OrderItemRequest]


class OrderItemResponse(BaseModel):
    product_id: str
    product_name: str
    unit_price: float
    quantity: int
    line_total: float


class OrderResponse(BaseModel):
    id: str
    user_id: str
    items: List[OrderItemResponse]
    total_price: float
    status: str
    
    
    
#OPSİYONELL    
#class tester()BaseModel:    
#
#    id: str
#    user_id: str
#    items: List[OrderItemResponse]
#    total_price: float
#    status: str  

  
