class Stocker:
    def __init__(self, id, stock_control):
        self.id = id
        self.stock_control = stock_control
    
    def __str__(self):
        return f"Stocker[id={self.id}, stock_control={self.stock_control}]"
