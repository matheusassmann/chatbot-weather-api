# app.py
from chalice import Chalice
from chatbot.message_parser import classify_message
from chatbot.weather_service import get_forecast
from chatbot import groq_client

app = Chalice(app_name='chatbot-weather-api')


@app.route("/", methods=["POST"])
def index():
    body = app.current_request.json_body
    message = body.get("message", "")

    classification = classify_message(message)

    if classification.get("weather"):
        city = classification.get("city", "São Paulo")
        forecast = get_forecast(city)
        return {"response": forecast}
    else:
        try:
            answer = groq_client.ask_llm(message)
            return {"response": answer}
        except Exception:
            return {"response": "Desculpe, não consegui obter uma resposta no momento."}
