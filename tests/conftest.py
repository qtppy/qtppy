import pytest
from qtpp import create_app

import warnings
warnings.filterwarnings("ignore")


@pytest.fixture
def app():
    app = create_app(config_name='test')

    return app

@pytest.fixture
def client(app):
    app.config['TESTING'] = True
    return app.test_client()

    def teardown():
        app.config['TESTING'] = False


@pytest.fixture
def runner(app):
    return app.test_cli_runner()



class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='xzdylyh', password='123456'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)