-- Tabela Clientes (Master)
CREATE TABLE Clientes (
    id_cliente NUMBER PRIMARY KEY,
    nome_cliente VARCHAR2(100),
    email_cliente VARCHAR2(100),
    telefone_cliente VARCHAR2(15)
);

-- Tabela Pedidos (Detail)
CREATE TABLE Pedidos (
    id_pedido NUMBER PRIMARY KEY,
    descricao_pedido VARCHAR2(255),
    valor_pedido NUMBER,
    id_cliente NUMBER,
    CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
);