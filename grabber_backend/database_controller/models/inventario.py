class Inventory:
    def __init__(self, product_id, product, locationX, locationY, quantity, id=None):
        self.id = id
        self.product_id = product_id
        self.product = product
        self.locationX = locationX
        self.locationY = locationY
        self.quantity = quantity
        
    def __str__(self):
        return f"Inventory[id={self.id}, product_id={self.product_id}, product={self.product}, locationX={self.locationX}, locationY={self.locationY}, quantity={self.quantity}]"
