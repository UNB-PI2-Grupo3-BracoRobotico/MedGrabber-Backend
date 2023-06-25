
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from grabber_backend.database_controller.models import carrinho, usuario, produto,inventario,pagamento,pedidos,estoquista,consumidor

class ModelTestCase(unittest.TestCase):
    def setUp(self):
        # Configurar a conexão com o banco de dados
        engine = create_engine('sqlite:///grabber.db')  # Substitua pelo seu banco de dados
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def tearDown(self):
        # Limpar os dados do banco de dados e fechar a sessão
        self.session.query(usuario).delete()
        self.session.query(produto).delete()
        self.session.query(inventario).delete()
        self.session.query(carrinho).delete()
        self.session.query(pagamento).delete()
        self.session.query(pedidos).delete()
        self.session.query(estoquista).delete()
        self.session.query(consumidor).delete()
        self.session.commit()
        self.session.close()

if __name__ == '__main__':
    unittest.main()
































# import unittest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.orm import declarative_base
# from grabber_backend.database_controller.models.models import produto, inventario, carrinho, pagamento, usuario, estoquista, pedidos, consumidor

# Base = declarative_base()

# class ModelsTestCase(unittest.TestCase):
#     def setUp(self):
#         # Configurar a conexão com o banco de dados de teste
#         engine = create_engine('sqlite:///test.db')
#         Session = sessionmaker(bind=engine)
#         self.session = Session()

#         # Criar as tabelas de teste
#         Base.metadata.create_all(engine)

#     def tearDown(self):
#         # Remover as tabelas de teste
#         Base.metadata.drop_all(self.session.bind)

#     def test_produto(self):
#         # Criar um objeto de Produto
#         product = produto(id=1, nome='Produto 1', preco=10.99, descricao='Descrição do Produto 1')

#         # Adicionar o objeto à sessão
#         self.session.add(product)
#         self.session.commit()

#         # Consultar o objeto da tabela Produto
#         product_consulted = self.session.query(produto).filter_by(id=1).first()

#         # Verificar se os valores são os mesmos
#         self.assertEqual(product_consulted.nome, 'Produto 1')
#         self.assertEqual(product_consulted.preco, 10.99)
#         self.assertEqual(product_consulted.descricao, 'Descrição do Produto 1')

#     def test_inventario(self):
#         # Criar um objeto de Inventario
#         inventory = inventario(id=1, id_Produto=1, localizacaoX=10.0, localizacaoY=20.0, quantidade=5)

#         # Adicionar o objeto à sessão
#         self.session.add(inventory)
#         self.session.commit()

#         # Consultar o objeto da tabela Inventario
#         inventory_consulted = self.session.query(inventario).filter_by(id=1).first()

#         # Verificar se os valores são os mesmos
#         self.assertEqual(inventory_consulted.id_Produto, 1)
#         self.assertEqual(inventory_consulted.localizacaoX, 10.0)
#         self.assertEqual(inventory_consulted.localizacaoY, 20.0)
#         self.assertEqual(inventory_consulted.quantidade, 5)

#     def test_carrinho(self):
#         # Criar um objeto de Carrinho
#         cart = carrinho(id=1, id_Produto=1, total=50.0)

#         # Adicionar o objeto à sessão
#         self.session.add(cart)
#         self.session.commit()

#         # Consultar o objeto da tabela Carrinho
#         cart_consulted = self.session.query(carrinho).filter_by(id=1).first()

#         # Verificar se os valores são os mesmos
#         self.assertEqual(cart_consulted.id_Produto, 1)
#         self.assertEqual(cart_consulted.total, 50.0)

#     def test_pagamento(self):
#         # Criar um objeto de Pagamento
#         payment = pagamento(id=1, id_Carrinho=1, status_pagamento=1, consumidor='João', tipoPagamento=2)

#         # Adicionar o objeto à sessão
#         self.session.add(payment)
#         self.session.commit()

#         # Consultar o objeto da tabela Pagamento
#         payment_consulted = self.session.query(pagamento).filter_by(id=1).first()

#         # Verificar se os valores são os mesmos
#         self.assertEqual(payment_consulted.id_Carrinho, 1)
#         self.assertEqual(payment_consulted.status_pagamento, 1)
#         self.assertEqual(payment_consulted.consumidor, 'João')
#         self.assertEqual(payment_consulted.tipoPagamento, 2)

#     def test_usuario(self):
#         # Criar um objeto de Usuario
#         user = usuario(cpf=1234567890, nome='João', login_usuario='joao', senha='senha123')

#         # Adicionar o objeto à sessão
#         self.session.add(user)
#         self.session.commit()

#         # Consultar o objeto da tabela Usuario
#         user_consulted = self.session.query(usuario).filter_by(cpf=1234567890).first()

#         # Verificar se os valores são os mesmos
#         self.assertEqual(user_consulted.nome, 'João')
#         self.assertEqual(user_consulted.login_usuario, 'joao')
#         self.assertEqual(user_consulted.senha, 'senha123')

#     def test_estoquista(self):
#         # Criar um objeto de Estoquista
#         stockist = estoquista(id=1, controleEstoque='Controle de Estoque')

#         # Adicionar o objeto à sessão
#         self.session.add(stockist)
#         self.session.commit()

#         # Consultar o objeto da tabela Estoquista
#         stockist_consulted = self.session.query(estoquista).filter_by(id=1).first()

#         # Verificar se os valores são os mesmos
#         self.assertEqual(stockist_consulted.controleEstoque, 'Controle de Estoque')

#     def test_pedidos(self):
#         # Criar um objeto de Pedidos
#         requests = pedidos(id=1, id_Pagamento=1, id_Carrinho=1, id_Usuario=1234567890, data_pedido=20220601, tipo='Normal')

#         # Adicionar o objeto à sessão
#         self.session.add(requests)
#         self.session.commit()

#         # Consultar o objeto da tabela Pedidos
#         requests_consulted = self.session.query(pedidos).filter_by(id=1).first()

#         # Verificar se os valores são os mesmos
#         self.assertEqual(requests_consulted.id_Pagamento, 1)
#         self.assertEqual(requests_consulted.id_Carrinho, 1)
#         self.assertEqual(requests_consulted.id_Usuario, 1234567890)
#         self.assertEqual(requests_consulted.data_pedido, 20220601)
#         self.assertEqual(requests_consulted.tipo, 'Normal')

#     def test_consumidor(self):
#         # Criar um objeto de Consumidor
#         consumer = consumidor(id=1, id_Carrinho=1, id_Pagamento=1)

#         # Adicionar o objeto à sessão
#         self.session.add(consumer)
#         self.session.commit()

#         # Consultar o objeto da tabela Consumidor
#         consumer_consulted = self.session.query(consumidor).filter_by(id=1).first()

#         # Verificar se os valores são os mesmos
#         self.assertEqual(consumer_consulted.id_Carrinho, 1)
#         self.assertEqual(consumer_consulted.id_Pagamento, 1)

# if __name__ == '__main__':
#     unittest.main()
