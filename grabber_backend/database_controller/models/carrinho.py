from sqlalchemy import Column, Integer, Float
from sqlalchemy.ext.declarative import declarative_base
import json

Base = declarative_base()

class Cart(Base):
    __tablename__ = "Cart"

    id = Column("id", Integer, primary_key=True)
    product = Column("product_id", Integer, nullable=False)
    total = Column("total", Float)

    def __eq__(self, other):
        if not isinstance(other, Cart):
            return False
        
        return (
            self.id == other.id and
            self.product == other.product and
            self.total == other.total
        )
    
    def __str__(self):
        return json.dumps({
            "id": self.id,
            "product": self.product,
            "total": self.total
        })

# class Cart:
#     def __init__(self, product_id, product, total, id=None):
#         self.id = id
#         self.product_id = product_id
#         self.product = product
#         self.total = total
    
#     def __str__(self):
#         return f"Cart[id={self.id}, product_id={self.product_id}, product={self.product}, total={self.total}]"