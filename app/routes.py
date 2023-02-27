from flask import flash, redirect, render_template, url_for, request
from flask_login import login_required, logout_user, login_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from .models import User, Telefone, Endereco, SolicitaColeta


def init_app(app):

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
