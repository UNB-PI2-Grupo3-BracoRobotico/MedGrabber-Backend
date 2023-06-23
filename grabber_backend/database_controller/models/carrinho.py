class Carrinho:
    def __init__(self, id_Produto, produto, total, id=None):
        self.id = id
        self.id_Produto = id_Produto
        self.produto = produto
        self.total = total
    
    def __str__(self):
        return f"Carrinho[id={self.id}, id_Produto={self.id_Produto}, produto={self.produto}, total={self.total}]"