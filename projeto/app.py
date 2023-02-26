from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager, UserMixin, \
    login_required, login_user, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from flask_bootstrap import Bootstrap
from datetime import datetime


app = Flask(__name__)


SECRET_KEY = "Alterar_secret_key"

app.config['SECRET_KEY'] = 'Secret_key_development'

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "postgresql://postgres:postgres@172.17.0.2/recicla"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

Bootstrap(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)

migrate = Migrate(app, db)


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


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/users")
@login_required
def users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/user/delete/<int:id>")
@login_required
def delete(id):
    """Rota deletar usuário"""
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("index"))


@app.route("/user/<int:id>")
@login_required
def perfil(id):
    """Rota listar perfil usuário"""
    user = User.query.get(id)
    endereco = Endereco.query.filter_by(user_id=id).first()
    telefone = Telefone.query.filter_by(user_id=id).first()
    return render_template(
        "user.html", user=user,
        endereco=endereco, telefone=telefone)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login de usuário"""
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Credenciais incorretas - E-mail', 'danger')
            return redirect(url_for('login'))
        if not check_password_hash(user.password, password):
            flash('Credenciais incorretas - senha', 'danger')
            return redirect(url_for('login'))
        login_user(user)
        return redirect(url_for('index'))
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Registro de usuários"""
    if request.method == "POST":
        user = User()
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.email = request.form['email']
        user.password = generate_password_hash(request.form['password'])
        db.session.add(user)
        db.session.commit()
        endereco = Endereco()
        endereco.street = request.form['street']
        endereco.numero = request.form['numero']
        endereco.bairro = request.form['bairro']
        endereco.cidade = request.form['cidade']
        endereco.estado = request.form['estado']
        endereco.cep = request.form['cep']
        endereco.user_id = user.id
        db.session.add(endereco)
        db.session.commit()
        telefone = Telefone()
        telefone.celular = request.form['celular']
        telefone.user_id = user.id
        db.session.add(telefone)
        db.session.commit()

        return redirect(url_for('login'))
    return render_template("register.html")


@app.route("/user/<int:id>/coleta/add", methods=["GET", "POST"])
@login_required
def coleta_usuario(id):
    user = User.query.get(id)

    if request.method == "POST":

        coleta = SolicitaColeta()
        coleta.tipo = request.form['tipo']
        coleta.quantidade = request.form['quantidade']
        coleta.situacao = request.form['situacao']
        coleta.descricao = request.form['descricao']
        db.session.add(coleta)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template(
        "coleta.html", user=user)


@app.route("/coleta/view")
@login_required
def view_coleta():
    solicita_coleta = SolicitaColeta.query.all()
    return render_template(
        "ordem_coleta.html",
        solicita_coleta=solicita_coleta
        )


@app.route("/coleta/view/<int:id>")
@login_required
def show_coleta(id):
    coleta = SolicitaColeta.query.get(id)

    return render_template(
        "show_coleta.html",
        coleta=coleta)


@app.route("/help")
def link_ajuda():
    return render_template("ajuda.html")


if __name__ == "__main__":
    app.run(debug=True)
