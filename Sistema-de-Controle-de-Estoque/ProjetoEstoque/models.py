from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Inicializar o banco sem associar ao app ainda
db = SQLAlchemy()

class Item(db.Model):
    __tablename__ = 'item'
    
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(100), unique=True, nullable=False, index=True)  # Adicionando índice
    nome = db.Column(db.String(100), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False, default=0)  # Definido valor padrão para 0
    preco = db.Column(db.Float, nullable=False, default=0.0)  # Definido valor padrão para 0
    data_entrada = db.Column(db.Date, nullable=False, default=datetime.utcnow)

    # Adicionando o método to_dict()
    def to_dict(self):
        return {
            'Código': self.codigo,
            'Nome': self.nome,
            'Quantidade': self.quantidade,
            'Preço': self.preco,
            'Data de Entrada': self.data_entrada.strftime('%Y-%m-%d')  # Formato de data como string
        }

    def __repr__(self):
        return f'<Item {self.codigo} - {self.nome}>'

class User(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Adicionado campo de e-mail
    senha_hash = db.Column(db.String(128), nullable=False)  # Aumentado tamanho para hash seguro
    data_criacao = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, senha):
        """Gera o hash da senha para armazenamento seguro"""
        self.senha_hash = generate_password_hash(senha)

    def check_password(self, senha):
        """Verifica a senha com o hash armazenado"""
        return check_password_hash(self.senha_hash, senha)

    def __repr__(self):
        return f'<User {self.nome}>'
