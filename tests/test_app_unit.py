from chalice.test import Client
from app import app
import json
import pytest
from unittest.mock import patch

@pytest.mark.unit
@patch("chalicelib.groq_client.ask_llm")
def test_regular_message(mock_ask):
    mock_ask.return_value = "A guitarra do Jimi Hendrix era uma Fender Stratocaster."
    
    with Client(app) as client:
        response = client.http.post(
            '/',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({"message": "Qual era a guitarra do Jimi Hendrix?"}).encode("utf-8")
        )
        assert response.status_code == 200
        assert 'fender' in response.json_body['response'].lower()

@pytest.mark.unit
@patch("chalicelib.weather_service.get_forecast")
def test_climate_message(mock_weather):
    mock_weather.return_value = {
        "min": 18.0,
        "max": 26.5,
        "date": "2025-05-20"
    }

    with Client(app) as client:
        response = client.http.post(
            '/',
            headers={'Content-Type': 'application/json'},
            body=json.dumps({"message": "Vai chover amanhã em Bertioga?"}).encode("utf-8")
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

        # Verificações de valor (exemplo)
        assert 10.0 <= resp['min'] <= 40.0
        assert 10.0 <= resp['max'] <= 50.0
