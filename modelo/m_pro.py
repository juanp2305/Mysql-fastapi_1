from typing import Optional
from pydantic import BaseModel

class producto(BaseModel):
    name: str
    price: Optional[int]
    stock: Optional[int]
    category_id: Optional[int] 
    
    
