from flask import Flask, request, jsonify
from twilio.rest import Client
import os
from flask_cors import CORS

app = Flask(__name__)
ALLOWED_ORIGIN = os.environ.get("ALLOWED_ORIGIN")

CORS(app, resources={
    r"/submit": {
        "origins": ALLOWED_ORIGIN
    }
})
# Twilio credentials from environment variables
ACCOUNT_SID = os.environ.get("TWILIO_SID")
AUTH_TOKEN = os.environ.get("TWILIO_AUTH")
WHATSAPP_FROM = os.environ.get("WHATSAPP_FROM")  # e.g., whatsapp:+14155238886
WHATSAPP_TO = os.environ.get("WHATSAPP_TO")      # e.g., whatsapp:+91XXXXXXXXXX

client = Client(ACCOUNT_SID, AUTH_TOKEN)

@app.route("/submit", methods=["POST"])
def submit_form():
    data = request.get_json()

    if not data or not data.get("name") or not data.get("email"):
        return jsonify({"error": "Name and Email are required"}), 400

    # Format message
    message_body = f"""
📩 New Form Submission
Name: {data['name']}
Email: {data['email']}
Message: {data.get('message', '')}
"""

    # Send via WhatsApp
    client.messages.create(
        body=message_body,
        from_=WHATSAPP_FROM,
        to=WHATSAPP_TO
    )

    return jsonify({"success": True, "message": "Form submitted and sent to WhatsApp!"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
