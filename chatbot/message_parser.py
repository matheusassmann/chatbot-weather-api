# chatbot/message_parser.py
import json
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def classify_message(message: str) -> dict:
    prompt = f"""
Você é um assistente que classifica mensagens. Diga se a mensagem é sobre previsão do tempo e, se for, extraia a cidade mencionada. Sempre responda no formato JSON abaixo.

Mensagem: "{message}"

Formato esperado:
{{
  "weather": true,
  "city": "Recife"
}}

Se não for sobre clima:
{{
  "weather": false
}}
"""

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.3
    }

    try:
        response = requests.post(GROQ_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        content = response.json()['choices'][0]['message']['content']

        # Tenta extrair o JSON retornado
        return json.loads(content)
    except Exception as e:
        return {"weather": False}
