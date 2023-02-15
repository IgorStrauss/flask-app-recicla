from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate


app = Flask(__name__)
SECRET_KEY = "Alterar_secret_key"


app.config["SQLALCHEMY_DATABASE_URI"] = \
    "postgresql://postgres:postgres@172.17.0.2/recicla"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

migrate = Migrate(app, db)


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40), nullable=False)
    password = db.Column(db.String(40), nullable=False)
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
    users = User.query.all()
    return render_template("users.html", users=users)


@app.route("/user/delete/<int:id>")
def delete(id):
    user = User.query.filter_by(id=id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("index"))


# @app.route("user/update/<int:id:")
# def update(id):
#     ...


@app.route("/user/<int:id>")
def perfil(id):
    user = User.query.get(id)
    endereco = Endereco.query.filter_by(user_id=id).first()
    telefone = Telefone.query.filter_by(user_id=id).first()
    return render_template(
        "user.html", user=user, endereco=endereco, telefone=telefone)


if __name__ == "__main__":
    app.run(debug=True)
