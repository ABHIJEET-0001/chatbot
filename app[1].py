from flask import Flask, request, Response
from twilio.rest import Client
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Initialize Twilio client
twilio_client = Client(
    os.getenv("TWILIO_ACCOUNT_SID"),
    os.getenv("TWILIO_AUTH_TOKEN")
)


@app.route('/whatsapp', methods=['POST'])
def whatsapp_reply():
    """Handle incoming WhatsApp messages and send AI responses"""
    try:
        # Extract incoming message
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')

        if not incoming_msg:
            return Response("Empty message", status=400)

        print(f"Received from {sender}: {incoming_msg}")

        # Get AI response from Groq
        headers = {
            "Authorization": f"Bearer {os.getenv('GROQ_API_KEY')}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "llama3-8b-8192",
            "messages": [{"role": "user", "content": incoming_msg}],
            "temperature": 0.7,
            "max_tokens": 1024
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=data,
            timeout=15
        )
        response.raise_for_status()

        reply = response.json()['choices'][0]['message']['content']
        print(f"AI Reply: {reply}")

        # Send response via WhatsApp
        message = twilio_client.messages.create(
            body=reply,
            from_=f"whatsapp:{os.getenv('TWILIO_WHATSAPP_NUMBER')}",
            to=f"whatsapp:{sender}"
        )

        return Response(status=200)

    except requests.exceptions.RequestException as e:
        print(f"API Error: {str(e)}")
        return Response("Service temporarily unavailable", status=503)
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return Response("Internal server error", status=500)


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )