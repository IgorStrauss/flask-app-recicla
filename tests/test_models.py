from app.models import User
from app import db 
from datetime import datetime


def test_new_user_with_fixture(new_user):

    assert new_user.first_name == 'Peter'
    assert new_user.id == 1
    assert new_user.last_name == 'Parker'
    assert new_user.email == 'spider@icloud.com'
    assert new_user.password_hashed != 'password'


def test_return_user_username():
    user = User()
    user.id = 1
    user.first_name = 'Peter'
    user.last_name = 'Parker'
    user.email = 'spider@icloud.com'
    user.password = 'password'
    user.criado = datetime.now()
    db.session.add(user)
    db.session.commit()

    assert user.id == 1
