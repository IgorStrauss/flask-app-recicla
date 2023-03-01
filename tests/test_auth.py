# import pytest
# from app import db
# from app.models import User


# def test_login(test_client):
#     user = User(username='test_user', email='test@example.com')
#     user.set_password('password')
#     db.session.add(user)
#     db.session.commit()

#     response = test_client.post('/login', data={
#         'username': 'test_user',
#         'password': 'password'
#     }, follow_redirects=True)

#     assert response.status_code == 200
#     assert b'Hello, test_user' in response.data
