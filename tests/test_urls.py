from app import create_app


def test_home_page():
    flask_app = create_app()

    with flask_app.test_client()as test_client:
        response = test_client.get('/')

        assert response.status_code == 200


def test_page_help():
    help = create_app()

    with help.test_client()as test_client:
        response = test_client.get('/help')

        assert response.status_code == 200


def test_page_users():
    """Usuário não autenticado"""
    users = create_app()

    with users.test_client()as test_client:
        response = test_client.get('/users')

        assert response.status_code == 401


def test_page_user_delete():
    """Usuário não autenticado"""
    user_delete = create_app()

    with user_delete.test_client()as test_client:
        response = test_client.get('/user/delete/1')

        assert response.status_code == 401


def test_page_user_perfil():
    """Usuário não autenticado"""
    user_perfil = create_app()

    with user_perfil.test_client()as test_client:
        response = test_client.get('/user/1')

        assert response.status_code == 401


def test_page_user_logout():
    """Usuário não autenticado"""
    user_logout = create_app()

    with user_logout.test_client()as test_client:
        response = test_client.get('/logout')

        assert response.status_code == 401


def test_page_user_request_collect():
    """Usuário não autenticado"""
    user_request_collect = create_app()

    with user_request_collect.test_client()as test_client:
        response = test_client.get('/user/1/coleta/add')

        assert response.status_code == 401


def test_page_user_view_collect():
    """Usuário não autenticado"""
    user_view_collect = create_app()

    with user_view_collect.test_client()as test_client:
        response = test_client.get('/coleta/view')

        assert response.status_code == 401


def test_page_user_view_collect_id():
    """Usuário não autenticado"""
    user_view_collect_id = create_app()

    with user_view_collect_id.test_client()as test_client:
        response = test_client.get('/coleta/view/1')

        assert response.status_code == 401


def test_home_page_post():
    home_page_post = create_app()
    with home_page_post.test_client()as test_client:
        response = test_client.post('/')

        assert response.status_code == 405
