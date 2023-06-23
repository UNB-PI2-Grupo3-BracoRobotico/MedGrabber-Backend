class Consumidor:
    def __init__(self, id_Carrinho, carrinho, id_Pagamento, pagamento, id=None):
        self.id = id
        self.id_Carrinho = id_Carrinho
        self.carrinho = carrinho
        self.id_Pagamento = id_Pagamento
        self.pagamento = pagamento
    
    def __str__(self):
        return f"Consumidor[id={self.id}, id_Carrinho={self.id_Carrinho}, carrinho={self.carrinho}, id_Pagamento={self.id_Pagamento}, pagamento={self.pagamento}]"