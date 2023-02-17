from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate
from flask_login import LoginManager, UserMixin, \
    login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
SECRET_KEY = "Alterar_secret_key"

app.config['SECRET_KEY'] = 'Secret_key_development'

app.config["SQLALCHEMY_DATABASE_URI"] = \
    "postgresql://postgres:postgres@172.17.0.2/recicla"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

migrate = Migrate(app, db)


@login_manager.user_loader
def current_user(user_id):
    """Confere usuário que estará logado"""
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    endereco = db.relationship('Endereco', backref='user', uselist=False)
    telefone = db.relationship('Telefone', backref='user', uselist=False)

    def __str__(self) -> str:
        return self.first_name

    @property
    def username(self):
        return f"{self.last_name}{self.first_name}".lower()


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
        return self.first_name


class Telefone(db.Model):
    __tablename__ = 'telefone'
    id = db.Column(db.Integer, primary_key=True)
    celular = db.Column(db.String(14), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __str__(self) -> str:
        return self.username


@app.route('/')
def index():
    return render_template("index.html")


@app.route("/users")
def users():
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/user/delete/<int:id>")
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
        "user.html", user=user, endereco=endereco, telefone=telefone)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Login de usuário"""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        
        if not user:
            flash('Credenciais incorretas')
            return redirect(url_for('login'))
        if not check_password_hash(user.password, password):
            flash('Credenciais incorretas - senha')
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
        telefone = Telefone()
        db.session.add(endereco)
        db.session.commit()
        telefone.celular = request.form['celular']
        telefone.user_id = user.id
        db.session.add(telefone)
        db.session.commit()
        return redirect(url_for('users'))
    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)
