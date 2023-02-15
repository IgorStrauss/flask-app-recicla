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

    def __str__(self) -> str:
        return self.first_name

    @property
    def username(self):
        return f"{self.last_name}{self.first_name}".lower()


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
    return render_template("user.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
