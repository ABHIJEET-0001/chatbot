
== AI WhatsApp Chatbot using LLaMA 3 API (Groq) ==

1. Install dependencies:
   pip install -r requirements.txt

2. Create a `.env` file with the following content:
   GROQ_API_KEY=your_groq_api_key
   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
   YOUR_WHATSAPP_NUMBER=whatsapp:+91xxxxxxxxxx

3. Start the Flask server:
   python app.py

4. Use ngrok to expose:
   ngrok http 5000
   Then set Twilio sandbox webhook to: https://<ngrok-url>/message

5. Send WhatsApp message to sandbox number and get reply from LLaMA 3.

Enjoy!
