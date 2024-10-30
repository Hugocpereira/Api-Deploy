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
        'password': 'senha123'
    })
    assert response.status_code == 200

def test_home_performance(benchmark, client):
    response = benchmark(client.get, '/')
    assert response.status_code == 200

def test_consulta_performance(benchmark, client):
    with app.app_context():  # Abre um contexto de aplicação
        # Cria o token de acesso dentro do contexto da aplicação
        access_token = create_access_token(identity="hugo")
        headers = {
            "Authorization": f"Bearer {access_token}"
        }

    # Usa o benchmark para medir o desempenho da requisição de consulta
    response = benchmark(client.get, '/consulta', headers=headers, query_string={
        'emp': '12345',
        'emp': '2385'
        
    })
    assert response.status_code == 200
