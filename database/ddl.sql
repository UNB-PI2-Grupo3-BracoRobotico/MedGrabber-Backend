CREATE TABLE IF NOT EXISTS Produto (
    id INT,
    nome VARCHAR(50),
    preco FLOAT,
    descricao VARCHAR(100),
    PRIMARY KEY(id)
);

CREATE TABLE IF NOT EXISTS Pagamento (
    id INT,
    consumidor VARCHAR(50),
    preco FLOAT,
    TipoPagamento VARCHAR(100),
    PRIMARY KEY(id)
);
