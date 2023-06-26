class Consumer:
    def __init__(self, cart_id, cart, payment_id, payment, id=None):
        self.id = id
        self.cart_id = cart_id
        self.cart = cart
        self.payment_id = payment_id
        self.payment = payment
    
    def __str__(self):
        return f"Consumer[id={self.id}, cart_id={self.cart_id}, cart={self.cart}, payment_id={self.payment_id}, payment={self.payment}]"
