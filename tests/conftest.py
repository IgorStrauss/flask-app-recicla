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

@pytest.fixture(scope='class')
def usuario(client):
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
def usuario_autenticado(usuario):
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


@pytest.fixture(scope='session')
def test_app():
    app.testing = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    db.create_all()
    yield app
    db.drop_all()


@pytest.fixture(scope='function')
def test_client(test_app):
    return test_app.test_client()
