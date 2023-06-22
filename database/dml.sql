-- Inserção de dados na tabela Produto
INSERT INTO Produto (id, nome, preco, descricao) VALUES (1, 'Produto 1', 10.99, 'Descrição do Produto 1');
INSERT INTO Produto (id, nome, preco, descricao) VALUES (2, 'Produto 2', 19.99, 'Descrição do Produto 2');
INSERT INTO Produto (id, nome, preco, descricao) VALUES (3, 'Produto 3', 5.99, 'Descrição do Produto 3');

-- Inserção de dados na tabela Inventario
INSERT INTO Inventario (id, id_Produto, localizacaoX, localizacaoY, quantidade) VALUES (1, 1, POINT(10, 20), POINT(30, 40), 100);
INSERT INTO Inventario (id, id_Produto, localizacaoX, localizacaoY, quantidade) VALUES (2, 2, POINT(50, 60), POINT(70, 80), 50);
INSERT INTO Inventario (id, id_Produto, localizacaoX, localizacaoY, quantidade) VALUES (3, 3, POINT(90, 100), POINT(110, 120), 200);

-- Inserção de dados na tabela Carrinho
INSERT INTO Carrinho (id, id_Produto, total) VALUES (1, 1, 10.99);
INSERT INTO Carrinho (id, id_Produto, total) VALUES (2, 2, 19.99);
INSERT INTO Carrinho (id, id_Produto, total) VALUES (3, 3, 5.99);

-- Inserção de dados na tabela Pagamento
INSERT INTO Pagamento (id, id_Carrinho, consumidor, tipoPagamento) VALUES (1, 1, 'João', 1);
INSERT INTO Pagamento (id, id_Carrinho, consumidor, tipoPagamento) VALUES (2, 2, 'Maria', 2);
INSERT INTO Pagamento (id, id_Carrinho, consumidor, tipoPagamento) VALUES (3, 3, 'Pedro', 1);

-- Inserção de dados na tabela Usuario
INSERT INTO Usuario (cpf, nome, login_usuario, senha) VALUES (123456789, 'Fulano', 'fulano123', 'senha123');
INSERT INTO Usuario (cpf, nome, login_usuario, senha) VALUES (987654321, 'Ciclano', 'ciclano456', 'senha456');

-- Inserção de dados na tabela Estoquista
INSERT INTO Estoquista (id, controleEstoque) VALUES (1, 'Controle de Estoque 1');
INSERT INTO Estoquista (id, controleEstoque) VALUES (2, 'Controle de Estoque 2');

-- Inserção de dados na tabela Pedidos
INSERT INTO Pedidos (id, id_Pagamento, id_Carrinho, id_Usuario, data_pedido, tipo) VALUES (1, 1, 1, 123456789, 20230605, 'Tipo 1');
INSERT INTO Pedidos (id, id_Pagamento, id_Carrinho, id_Usuario, data_pedido, tipo) VALUES (2, 2, 2, 987654321, 20230605, 'Tipo 2');

-- Inserção de dados na tabela consumidor
INSERT INTO consumidor (id, id_Carrinho, id_Pagamento) VALUES (1, 1, 1);
INSERT INTO consumidor (id, id_Carrinho, id_Pagamento) VALUES (2, 2, 2);
