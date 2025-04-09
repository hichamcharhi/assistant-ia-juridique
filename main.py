from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os

app = FastAPI()

# Autoriser tous les domaines (ex. assistant.hichamcharhi.com)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")

    headers = {
        "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
        "HTTP-Referer": "https://assistant.hichamcharhi.com",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content":
             "Tu es un assistant juridique intelligent formé par Hicham CHARHI. "
             "Tu aides à comprendre les enjeux de l'encadrement juridique de l'intelligence artificielle, "
             "notamment en droit privé marocain, européen et international. "
             "Réponds de manière claire, rigoureuse et académique."},
            {"role": "user", "content": message}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        result = response.json()
        return {"response": result["choices"][0]["message"]["content"]}
    except Exception as e:
        return {"error": str(e)}
