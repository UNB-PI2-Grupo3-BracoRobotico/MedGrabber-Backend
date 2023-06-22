-- Adição de tabelas
CREATE TABLE IF NOT EXISTS Produto (
    id INT,
    nome VARCHAR(100),
    preco FLOAT,
    descricao VARCHAR(100),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Inventario (
    id INT,
    id_Produto INT,
    localizacaoX POINT,
    localizacaoY POINT,
    quantidade INT,
    PRIMARY KEY(id),
    CONSTRAINT fk_Produto FOREIGN KEY (id_Produto) REFERENCES Produto(id)
);

CREATE TABLE IF NOT EXISTS Carrinho (
    id INT,
    id_Produto INT,
    total FLOAT,
    PRIMARY KEY(id), 
    CONSTRAINT fk_Produto FOREIGN KEY (id_Produto) REFERENCES Produto(id)
);

CREATE TABLE IF NOT EXISTS Pagamento(
    id INT,
    id_Carrinho INT,
    status_pagamento integer not null default 0,
    consumidor VARCHAR(100),
    tipoPagamento INT,
    PRIMARY KEY(id),
    CONSTRAINT fk_Carrinho FOREIGN KEY (id_Carrinho) REFERENCES Carrinho(id)
);

CREATE TABLE IF NOT EXISTS Usuario(
    cpf INT,
    nome VARCHAR(100),
    login_usuario VARCHAR(100),
    senha VARCHAR(100),
    PRIMARY KEY(cpf)
);

CREATE TABLE IF NOT EXISTS Estoquista(
    id INT,
    controleEstoque VARCHAR(100),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Pedidos(
    id INT,
    id_Pagamento INT,
    id_Carrinho INT,
    id_Usuario INT,
    data_pedido INT,
    tipo VARCHAR(50),
    PRIMARY KEY(id),
    CONSTRAINT fk_Pagamento FOREIGN KEY (id_Pagamento) REFERENCES Pagamento(id),
    CONSTRAINT fk_Carrinho FOREIGN KEY (id_Carrinho) REFERENCES Carrinho(id),
    CONSTRAINT fk_Usuario FOREIGN KEY (id_Usuario) REFERENCES Usuario(cpf)
);

CREATE TABLE IF NOT EXISTS consumidor(
    id INT,
    id_Carrinho INT,
    id_Pagamento INT,
    PRIMARY KEY(id),
    CONSTRAINT fk_Carrinho FOREIGN KEY (id_Carrinho) REFERENCES Carrinho(id),
    CONSTRAINT fk_Pagamento FOREIGN KEY (id_Pagamento) REFERENCES Pagamento(id)
);

