from typing import Optional

from pydantic import BaseModel


class Order(BaseModel):
    order_id: int
    customer_id: int
    status: Optional[str] = "received"
    item_list: list[dict]
    total_price: str
    payment_method: str
    timestamp: str
