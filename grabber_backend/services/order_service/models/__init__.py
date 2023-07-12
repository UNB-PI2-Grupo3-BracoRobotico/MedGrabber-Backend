from typing import Optional

from pydantic import BaseModel


class ServiceOrder(BaseModel):
    id: Optional[int] = None
    user: str
    order_status: Optional[str] = "awaiting_payment"
    order_items: list[dict]
    total_price: float
    payment_method: str
    order_date: Optional[int] = None
