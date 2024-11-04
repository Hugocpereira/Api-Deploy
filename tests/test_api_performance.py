import pytest
from API_PLAM import create_app
from flask_jwt_extended import create_access_token

app = create_app()
app.config['TESTING'] = True

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_login_performance(benchmark, client):
    response = benchmark(client.post, '/login', json={
        'username': 'hugo',
        'password': 'senhasenha'
    })
    assert response.status_code == 200
    assert 'token' in response.json 

def test_home_performance(benchmark, client):
    response = benchmark(client.get, '/')
    assert response.status_code == 200

def test_consulta_performance(benchmark, client):
    with app.app_context():  
        access_token = create_access_token(identity="hugo")
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

    response = benchmark(client.get, '/api/consulta', headers=headers, query_string={
        'emp': '12345',
        'ben': '2385'
    })
    assert response.status_code == 200

def test_login_invalid_user(client):
    response = client.post('/login', json={
        'username': 'invalido',
        'password': 'senhaerrada'
    })
    assert response.status_code == 401  
