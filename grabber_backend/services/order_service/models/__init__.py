from typing import Optional

from pydantic import BaseModel


class Order(BaseModel):
    id: int
    user: str
    status: Optional[str] = "received"
    order_items: list[dict]
    total_price: str
    payment_method: str
    timestamp: Optional[int]
