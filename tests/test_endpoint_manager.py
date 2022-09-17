import pytest
from app.db import get_db


def test_index(client, auth):
    #response = client.get('/')
    #assert b"Log In" in response.data
    #assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    #assert b'test name' in response.data
    assert b'by test on 2018-01-01' in response.data
    assert b'test\ndata' in response.data
    assert b'href="/1/update"' in response.data


@pytest.mark.parametrize('path', (
    '/upload',
    '/1/update',
    '/1/delete',
))
def test_login_required(client, path):
    response = client.post(path)
    assert response.headers["Location"] == "/auth/login"


def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE endpoints SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/1/update').status_code == 403
    assert client.post('/1/delete').status_code == 403
    # current user doesn't see edit link
    assert b'href="/1/update"' not in client.get('/').data


@pytest.mark.parametrize('path', (
    '/3/update',
    '/3/delete',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path).status_code == 404


def test_token_generation(client, auth):
    auth.login()
    assert client.get('/auth/client_access').status_code == 200

    # Check if Admin option is displayed
    assert b'<option value="0">' in client.get('/auth/client_access').data
    assert b'Admin' in client.get('/auth/client_access').data

    # Check if api option is displayed
    assert b'<option value="1">' in client.get('/auth/client_access').data
    assert b'/api/fetch/test_name (Public)' in client.get('/auth/client_access').data

    # Test creating admin token
    client.post('/auth/client_access',
                data={'submit': 'Generate',
                      'endpoint_access_id': 0,
                      'access_limit': 10})

    assert b'Admin token - Client id:' in client.get('/auth/client_access').data
    assert b' Expiry: 2018-01-11 00:00:00'

    # Test creating api token
    client.post('/auth/client_access',
                data={'submit': 'Generate',
                      'endpoint_access_id': 1,
                      'access_limit': 20})

    assert b'/api/fetch/test_name - Client id:' in client.get('/auth/client_access').data
    assert b' Expiry: 2018-01-21 00:00:00'

    # Test presence of existing token
    assert b'Client id: test' in client.get('/auth/client_access').data

    # Test delete existing token
    client.post('/auth/client_access',
                data={'submit': 'Delete',
                      'delete_token': 'test',
                      'access_limit': 10})

    # Test absence of existing token
    assert b'Client id: test' not in client.get('/auth/client_access').data


def test_token_access(app, client, auth):
    auth.login()
    # Test creating admin token
    client.post('/auth/client_access',
                data={'submit': 'Generate',
                      'endpoint_access_id': 0,
                      'access_limit': 10})

    with app.app_context():
        db = get_db()
        access = db.execute('SELECT read_access, write_access, create_access, delete_access from client_access '
                            'where endpoint_access_id = 0 and id = 2').fetchone()
        db.commit()

        assert access['read_access'] == 'TRUE'
        assert access['write_access'] == 'TRUE'
        assert access['create_access'] == 'TRUE'
        assert access['delete_access'] == 'TRUE'

    # Test creating api token
    client.post('/auth/client_access',
                data={'submit': 'Generate',
                      'endpoint_access_id': 1,
                      'access_limit': 20})

    with app.app_context():
        db = get_db()
        access = db.execute(
            'SELECT read_access, write_access, create_access, delete_access from client_access '
            'where endpoint_access_id = 1 and id = 3').fetchone()
        db.commit()

        assert access['read_access'] == 'TRUE'
        assert access['write_access'] == 'FALSE'
        assert access['create_access'] == 'FALSE'
        assert access['delete_access'] == 'FALSE'


# Test absence of other users endpoints
def test_user_endpoints(client, auth):
    auth.login()
    response = client.get('/')

    assert b'/api/fetch/test_name' in response.data
    assert b'/api/fetch/test_name_2' not in response.data


def test_delete(client, auth, app):
    auth.login()
    response = client.post('/1/delete')
    assert response.headers["Location"] == "/"

    with app.app_context():
        db = get_db()
        post = db.execute('SELECT * FROM endpoints WHERE id = 1').fetchone()
        assert post is None

