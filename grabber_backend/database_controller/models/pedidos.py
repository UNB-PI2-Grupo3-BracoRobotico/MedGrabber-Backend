class Pedidos:
    def __init__(self, id_Pagamento, pagamento, id_Carrinho, carrinho, id_Usuario, usuario, data_pedido, tipo, id=None):
        self.id = id
        self.id_Pagamento = id_Pagamento
        self.pagamento = pagamento
        self.id_Carrinho = id_Carrinho
        self.carrinho = carrinho
        self.id_Usuario = id_Usuario
        self.usuario = usuario
        self.data_pedido = data_pedido
        self.tipo = tipo
    
    def __str__(self):
        return f"Pedidos[id={self.id}, id_Pagamento={self.id_Pagamento}, pagamento={self.pagamento}, id_Carrinho={self.id_Carrinho}, carrinho={self.carrinho}, id_Usuario={self.id_Usuario},usuario={self.usuario}, data_pedido={self.data_pedido}, tipo={self.tipo}]"