from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)

# Configuração de conexão com Oracle usando oracledb como driver
DATABASE_URL = "oracle+oracledb://rm97850:120803@oracle.fiap.com.br:1521/ORCL"

# Criação do engine
engine = create_engine(DATABASE_URL, echo=True)

# Criar sessão e base para os modelos
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Definição das tabelas usando SQLAlchemy
class Cliente(Base):
    __tablename__ = 'CLIENTES'  
    id_cliente = Column(Integer, primary_key=True)
    nome_cliente = Column(String(100))
    email_cliente = Column(String(100))
    telefone_cliente = Column(String(15))
    pedidos = relationship("Pedido", back_populates="cliente")

class Pedido(Base):
    __tablename__ = 'PEDIDOS'  
    id_pedido = Column(Integer, primary_key=True)
    descricao_pedido = Column(String(255))
    valor_pedido = Column(Float)
    id_cliente = Column(Integer, ForeignKey('CLIENTES.id_cliente'))  
    cliente = relationship("Cliente", back_populates="pedidos")

# Inicializar o banco de dados (se necessário)
# Comente se as tabelas já existem
# Base.metadata.create_all(engine)

# CRUD Clientes
@app.route('/clientes', methods=['GET'])
def get_clientes():
    session = Session()
    clientes = session.query(Cliente).all()
    result = [{"id_cliente": c.id_cliente, "nome_cliente": c.nome_cliente, "email_cliente": c.email_cliente, "telefone_cliente": c.telefone_cliente} for c in clientes]
    session.close()
    return jsonify(result)

@app.route('/clientes', methods=['POST'])
def create_cliente():
    session = Session()
    data = request.json
    novo_cliente = Cliente(id_cliente=data['id_cliente'], nome_cliente=data['nome_cliente'], email_cliente=data['email_cliente'], telefone_cliente=data['telefone_cliente'])
    session.add(novo_cliente)
    session.commit()
    session.close()
    return jsonify({"message": "Cliente criado com sucesso!"}), 201

@app.route('/clientes/<int:id_cliente>', methods=['PUT'])
def update_cliente(id_cliente):
    session = Session()
    data = request.json
    cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
    if not cliente:
        session.close()
        return jsonify({"message": "Cliente não encontrado"}), 404
    cliente.nome_cliente = data['nome_cliente']
    cliente.email_cliente = data['email_cliente']
    cliente.telefone_cliente = data['telefone_cliente']
    session.commit()
    session.close()
    return jsonify({"message": "Cliente atualizado com sucesso!"})

@app.route('/clientes/<int:id_cliente>', methods=['DELETE'])
def delete_cliente(id_cliente):
    session = Session()
    cliente = session.query(Cliente).filter_by(id_cliente=id_cliente).first()
    if not cliente:
        session.close()
        return jsonify({"message": "Cliente não encontrado"}), 404
    session.delete(cliente)
    session.commit()
    session.close()
    return jsonify({"message": "Cliente deletado com sucesso!"})

# CRUD Pedidos
@app.route('/pedidos', methods=['GET'])
def get_pedidos():
    session = Session()
    pedidos = session.query(Pedido).all()
    result = [{"id_pedido": p.id_pedido, "descricao_pedido": p.descricao_pedido, "valor_pedido": p.valor_pedido, "id_cliente": p.id_cliente} for p in pedidos]
    session.close()
    return jsonify(result)

@app.route('/pedidos', methods=['POST'])
def create_pedido():
    session = Session()
    data = request.json
    novo_pedido = Pedido(id_pedido=data['id_pedido'], descricao_pedido=data['descricao_pedido'], valor_pedido=data['valor_pedido'], id_cliente=data['id_cliente'])
    session.add(novo_pedido)
    session.commit()
    session.close()
    return jsonify({"message": "Pedido criado com sucesso!"}), 201

@app.route('/pedidos/<int:id_pedido>', methods=['PUT'])
def update_pedido(id_pedido):
    session = Session()
    data = request.json
    pedido = session.query(Pedido).filter_by(id_pedido=id_pedido).first()
    if not pedido:
        session.close()
        return jsonify({"message": "Pedido não encontrado"}), 404
    pedido.descricao_pedido = data['descricao_pedido']
    pedido.valor_pedido = data['valor_pedido']
    session.commit()
    session.close()
    return jsonify({"message": "Pedido atualizado com sucesso!"})

@app.route('/pedidos/<int:id_pedido>', methods=['DELETE'])
def delete_pedido(id_pedido):
    session = Session()
    pedido = session.query(Pedido).filter_by(id_pedido=id_pedido).first()
    if not pedido:
        session.close()
        return jsonify({"message": "Pedido não encontrado"}), 404
    session.delete(pedido)
    session.commit()
    session.close()
    return jsonify({"message": "Pedido deletado com sucesso!"})

if __name__ == '__main__':
    app.run(debug=True)
