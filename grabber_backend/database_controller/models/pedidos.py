class Orders:
    def __init__(self, payment_id, payment, cart_id, cart, user_id, user, order_date, order_type, id=None):
        self.id = id
        self.payment_id = payment_id
        self.payment = payment
        self.cart_id = cart_id
        self.cart = cart
        self.user_id = user_id
        self.user = user
        self.order_date = order_date
        self.order_type = order_type
    
    def __str__(self):
        return f"Orders[id={self.id}, payment_id={self.payment_id}, payment={self.payment}, cart_id={self.cart_id}, cart={self.cart}, user_id={self.user_id}, user={self.user}, order_date={self.order_date}, order_type={self.order_type}]"
