
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
