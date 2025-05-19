from chalice.test import Client
from app import app
import json
import pytest

@pytest.mark.integration
def test_real_climate_message():
    """Deve retornar previsão do tempo ao perguntar sobre clima"""
    with Client(app) as client:
        response = client.http.post(
            '/',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({"message": "vai chover em Bertioga amanhã?"}).encode("utf-8")
        )

        assert response.status_code == 200
        
        resp = response.json_body['response']

        # Verificações estruturais
        assert isinstance(resp, dict)
        assert 'min' in resp and 'max' in resp and 'date' in resp

        # Verificações de tipo
        assert isinstance(resp['min'], (int, float))
        assert isinstance(resp['max'], (int, float))
        assert isinstance(resp['date'], str)

        # Verificações opcionais de valor
        assert 10.0 <= resp['min'] <= 50.0
        assert 10.0 <= resp['max'] <= 60.0

@pytest.mark.integration
def test_real_regular_message():
    """Deve retornar resposta genérica ao perguntar algo comum"""
    with Client(app) as client:
        response = client.http.post(
            '/',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({"message": "Qual era a guitarra do Jimi Hendrix?"}).encode("utf-8")
        )
        assert response.status_code == 200
        assert 'fender' in response.json_body['response'].lower() or 'stratocaster' in response.json_body['response'].lower()
