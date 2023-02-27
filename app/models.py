from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def current_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    criado = db.Column(db.DateTime, nullable=False)
    endereco = db.relationship('Endereco', backref='user', uselist=False)
    telefone = db.relationship('Telefone', backref='user', uselist=False)
    solicitar_coleta = db.relationship(
        'SolicitaColeta', backref='user', uselist=False)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.criado = datetime.now()

    @property
    def formata_data(self):
        return f"{self.criado.day}/{self.criado.month}/{self.criado.year} as \
            {self.criado.hour}:{self.criado.minute}"

    def __str__(self):
        return self.first_name

    @property
    def firstname(self):
        return f"{self.first_name}".title()

    @property
    def lastname(self):
        return f"{self.last_name}".title()

    @property
    def username(self):
        return f"{self.last_name}{self.first_name}".upper()


class Endereco(db.Model):
    __tablename__ = "endereco"
    id = db.Column(db.Integer, primary_key=True)
    street = db.Column(db.String(30), nullable=False)
    numero = db.Column(db.String(8), nullable=False)
    bairro = db.Column(db.String(30), nullable=False)
    cidade = db.Column(db.String(30), nullable=False)
    estado = db.Column(db.String(30), nullable=False)
    cep = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __str__(self) -> str:
        return self.__name__


class Telefone(db.Model):
    __tablename__ = 'telefone'
    id = db.Column(db.Integer, primary_key=True)
    celular = db.Column(db.String(14), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __str__(self) -> str:
        return self.__name__

    @property
    def formata_celular(self):
        return f"({self.celular[:2]})\
            {self.celular[2]} {self.celular[3:7]}-{self.celular[7:]}"


class SolicitaColeta(db.Model):
    __tablename__ = 'solicitar_coleta'
    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    quantidade = db.Column(db.String(2), nullable=False)
    situacao = db.Column(db.String(50))
    descricao = db.Column(db.String(100))
    criado = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __init__(self, *args, **kwargs) -> None:
        super().__init__()
        self.criado = datetime.now()

    @property
    def formata_data(self):
        return f"{self.criado.day}/{self.criado.month}/{self.criado.year} ás \
            {self.criado.hour}:{self.criado.minute}"

    def formata_tipo(self):
        return {self.tipo}.title()

    def formata_situacao(self):
        return {self.situacao}.title()

    def formata_descricao(self):
        return {self.descricao}.title()
