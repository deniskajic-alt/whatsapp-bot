from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

# Link tvog Google Sheeta kao CSV (zamijeni s tvojim)
SHEET_URL = "https://docs.google.com/spreadsheets/d/1k2gQ2yq3N7dPxTTN2ra4kHEGA6jnhSE5eguf-cf0Z8Q/export?format=csv"

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    incoming_msg = request.values.get("Body", "").strip().lower()
    resp = MessagingResponse()
    msg = resp.message()

    # Preuzmi zadatke iz Google Sheeta
    r = requests.get(SHEET_URL)
    lines = r.text.split("\n")[1:]  # preskoči header

    if "zadaca" in incoming_msg or "compito" in incoming_msg:
        found = []
        for row in lines:
            if not row.strip():
                continue
            giorno, materia, compito = row.split(",")
            found.append(f"{giorno.strip().capitalize()}: {materia.strip()} — {compito.strip()}")
        msg.body("\n".join(found))
    else:
        msg.body("Ciao! Pošalji poruku 'zadaca' ili 'compito' da vidiš zadatke 📚")
    
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
