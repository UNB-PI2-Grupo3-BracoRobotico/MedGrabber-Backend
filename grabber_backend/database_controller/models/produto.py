class Produto:
    def __init__(self, nome, preco, descricao, id=None):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.descricao = descricao
      
    def __str__(self):
        return f"Produto[id={self.id}, nome={self.nome}, preco={self}, descricao={self.descricao}]"