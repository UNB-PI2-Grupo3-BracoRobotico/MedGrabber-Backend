class Inventario:
    def __init__(self, id_Produto, produto, localizacaoX, localizacaoY, quantidade, id=None):
        self.id = id
        self.id_Produto = id_Produto
        self.produto = produto
        self.localizacaoX = localizacaoX
        self.localizacaoY = localizacaoY
        self.quantidade = quantidade
        
    def __str__(self):
        return f"Inventario[id={self.id}, id_Produto={self.id_Produto}, produto={self.produto}, localizacaoX={self.localizacaoX}, localizacaoY={self.localizacaoY}, quantidade={self.quantidade}]"
