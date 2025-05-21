# chalicelib/groq_client.py
import requests
from datetime import datetime
from chalicelib.weather_service import get_forecast
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def ask_llm(message: str) -> str:
    system_prompt = (
        "Você é um assistente de chatbot. "
        "Seu papel é detectar se a mensagem do usuário está perguntando sobre o clima "
        "e, se sim, identificar a cidade mencionada. "
        "Retorne apenas a cidade (em texto simples), sem explicações extras. "
        "Se a pergunta não for sobre clima, responda com 'GENERIC'."
    )

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ],
        "temperature": 0.2
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload)
        response.raise_for_status()

        city_or_generic = response.json()['choices'][0]['message']['content'].strip()

        if city_or_generic.upper() == "GENERIC":
            return ask_generic(message)

        forecast = get_forecast(city_or_generic)

        if isinstance(forecast, dict) and "date" in forecast:
            date_str = forecast['date']
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d/%m/%Y")
            except ValueError:
                formatted_date = date_str  # fallback se formato inesperado

            return (
                f"A previsão para {city_or_generic} em {formatted_date} "
                f"é de mínima de {forecast['min']}°C e máxima de {forecast['max']}°C."
            )
        else:
            return forecast  # Caso forecast não seja um dict esperado

    except (requests.RequestException, KeyError, IndexError, TypeError) as e:
        return f"Ocorreu um erro ao processar a solicitação: {str(e)}"


def ask_generic(message: str) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": message}],
        "temperature": 0.7
    }

    response = requests.post(GROQ_API_URL, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()['choices'][0]['message']['content'].strip()
