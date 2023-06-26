class Product:
    def __init__(self, name, price, description, id=None):
        self.id = id
        self.name = name
        self.price = price
        self.description = description
      
    def __str__(self):
        return f"Product[id={self.id}, name={self.name}, price={self.price}, description={self.description}]"
