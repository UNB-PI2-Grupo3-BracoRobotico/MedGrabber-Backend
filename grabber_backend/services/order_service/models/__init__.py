from typing import Optional

from pydantic import BaseModel

class Item(BaseModel):
    item_id: int
    quantity: int

class Order(BaseModel):
    order_id: int
    customer_id: int
    status: Optional[str] = 'received'
    item_list: list[Item]
    total_price: str
    payment_method: str
    timestamp: str