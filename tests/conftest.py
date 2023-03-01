import app
import pytest
from datetime import datetime
from app import create_app
from app.models import User, Telefone, Endereco, SolicitaColeta
from app import db
from flask_login import LoginManager, login_user, current_user


@pytest.fixture(scope="module")
def app():
    return create_app()


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQL_DATABASE_URI"] = "sqlite:///"
    app.config["WTF_CSRF_ENABLED"] = False
    context = app.app_context()
    context.push

    db.create_all()

    yield app.test_client()

    db.session.remove()
    db.drop_all()

    context.pop()


@pytest.fixture(scope='class')
def user():
    user = User()
    user.first_name = 'peter'
    user.last_name = 'parker'
    user.email = 'spider@icloud.com'
    user.password = 'password'
    user.criado = datetime.now()
    yield user
    del user

@pytest.fixture
def usuario():
    app.testing = True
    client = app.test_client()
    usuario = User()
    usuario.id = 1
    usuario.first_name = 'peter'
    usuario.last_name = 'parker'
    usuario.email = 'spider@icloud.com'
    usuario.criado = datetime.now()
    db.session.add(usuario)
    db.session.commit()
    with client:
        login_user(usuario)
    yield client
    db.session.delete(usuario)
    db.session.commit()


@pytest.fixture
def usuario_autenticado():
    assert current_user.is_authenticated
    return usuario


@pytest.fixture(scope='class')
def telefone():
    fone = Telefone()
    fone.celular = '11912345678'
    yield fone
    del fone


@pytest.fixture(scope='class')
def endereco():
    endereco = Endereco()
    endereco.street = 'Rua A'
    endereco.bairro = 'Bairro A'
    endereco.cidade = 'Cidade A'
    endereco.estado = 'BR'
    endereco.cep = '01234999'
    yield endereco
    del endereco


@pytest.fixture(scope='class')
def coleta():
    coleta = SolicitaColeta()
    coleta.tipo = 'produto'
    coleta.quantidade = 1
    coleta.descricao = 'descrição'
    coleta.situacao = 'situação'
    coleta.criado = datetime.now()
    yield coleta
    del coleta
