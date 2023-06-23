class Estoquista:
    def __init__(self, id, controleEstoque):
        self.id = id
        self.controleEstoque = controleEstoque
    
    def __str__(self):
        return f"Estoquista[id={self.id}, controleEstoque={self.controleEstoque}]"