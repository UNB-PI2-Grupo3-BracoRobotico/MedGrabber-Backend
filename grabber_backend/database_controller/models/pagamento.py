class Pagamento:
    def __init__(self, id_Carrinho, carrinho, status_pagamento, consumidor, tipoPagamento, id=None):
        self.id = id
        self.id_Carrinho = id_Carrinho
        self.carrinho = carrinho
        self.status_pagamento = status_pagamento
        self.consumidor = consumidor
        self.tipoPagamento = tipoPagamento
    
    def __str__(self):
        return f"Pagamento[id={self.id}, id_Carrinho={self.id_Carrinho}, carrinho={self.carrinho}, status_pagamento={self.status_pagamento}, consumidor={self.consumidor}, tipoPagamento={self.tipoPagamento}]"