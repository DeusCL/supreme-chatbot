from fastapi import FastAPI, Request
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os

from gemini_chatbot import GeminiChatBot

load_dotenv()

ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')

IA_API_KEY = os.getenv('GEMINI_API_KEY')
IA_MODEL = os.getenv('GEMINI_MODEL')

client = Client(ACCOUNT_SID, AUTH_TOKEN)
chatbot = GeminiChatBot(IA_API_KEY)

app = FastAPI()

@app.post("/webhook")
async def receive_message(request: Request):
    form_data = await request.form()

    body = form_data.get("Body", "")
    sender = form_data.get("From", "")

    if "/reset" in body:
        chatbot.reset_history(sender)
        response = "Chatbot reseteao."
    else:
        response = chatbot.send(body, sender, IA_MODEL)

    client.messages.create(
        body=response,
        from_=PHONE_NUMBER,
        to=sender
    )

    return {"message": "Mensaje recibido y respuesta enviada"}


@app.get("/test")
async def test():
    return {"message": "Funcionando."}


# Para ejecutar el servidor de desarrollo
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

