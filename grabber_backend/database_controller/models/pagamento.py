class Payment:
    def __init__(self, cart_id, cart, payment_status, consumer, payment_type, id=None):
        self.id = id
        self.cart_id = cart_id
        self.cart = cart
        self.payment_status = payment_status
        self.consumer = consumer
        self.payment_type = payment_type
    
    def __str__(self):
        return f"Payment[id={self.id}, cart_id={self.cart_id}, cart={self.cart}, payment_status={self.payment_status}, consumer={self.consumer}, payment_type={self.payment_type}]"
