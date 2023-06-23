# from sqlalchemy import Column, Integer, String, Float, ForeignKey
# from sqlalchemy.orm import relationship
# from sqlalchemy.orm import declarative_base

# Base = declarative_base()

# class produto(Base):
#     __tablename__ = 'produto'
#     id = Column(Integer, primary_key=True)
#     nome = Column(String(100))
#     preco = Column(Float)
#     descricao = Column(String(100))

# class inventario(Base):
#     __tablename__ = 'inventario'
#     id = Column(Integer, primary_key=True)
#     id_Produto = Column(Integer, ForeignKey('produto.id'))
#     produto = relationship('produto', backref='inventario')
#     localizacaoX = Column(Float)
#     localizacaoY = Column(Float)
#     quantidade = Column(Integer)

# class carrinho(Base):
#     __tablename__ = 'carrinho'
#     id = Column(Integer, primary_key=True)
#     id_Produto = Column(Integer, ForeignKey('produto.id'))
#     produto = relationship('produto', backref='carrinho')
#     total = Column(Float)

# class pagamento(Base):
#     __tablename__ = 'pagamento'
#     id = Column(Integer, primary_key=True)
#     id_Carrinho = Column(Integer, ForeignKey('carrinho.id'))
#     carrinho = relationship('carrinho', backref='pagamento')
#     status_pagamento = Column(Integer, default=0)
#     consumidor = Column(String(100))
#     tipoPagamento = Column(Integer)

# class usuario(Base):
#     __tablename__ = 'usuario'
#     cpf = Column(Integer, primary_key=True)
#     nome = Column(String(100))
#     login_usuario = Column(String(100))
#     senha = Column(String(100))

# class estoquista(Base):
#     __tablename__ = 'estoquista'
#     id = Column(Integer, primary_key=True)
#     controleEstoque = Column(String(100))

# class pedidos(Base):
#     __tablename__ = 'pedidos'
#     id = Column(Integer, primary_key=True)
#     id_Pagamento = Column(Integer, ForeignKey('pagamento.id'))
#     pagamento = relationship('pagamento', backref='pedidos')
#     id_Carrinho = Column(Integer, ForeignKey('carrinho.id'))
#     carrinho = relationship('carrinho', backref='pedidos')
#     id_Usuario = Column(Integer, ForeignKey('usuario.cpf'))
#     usuario = relationship('usuario', backref='pedidos')
#     data_pedido = Column(Integer)
#     tipo = Column(String(50))

# class consumidor(Base):
#     __tablename__ = 'consumidor'
#     id = Column(Integer, primary_key=True)
#     id_Carrinho = Column(Integer, ForeignKey('carrinho.id'))
#     carrinho = relationship('carrinho', backref='consumidor_carrinho')
#     id_Pagamento = Column(Integer, ForeignKey('pagamento.id'))
#     pagamento = relationship('pagamento', backref='consumidor_pagamento')
