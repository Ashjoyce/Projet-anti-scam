from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_socketio import SocketIO, emit
from google.cloud import texttospeech
import openai
import os
import random
import logging

# --- Configuration ---
# Clé API OpenAI
openai.api_key = "eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTYyMDQwMjcwMTg4NDk2NDk1MSIsInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIiwiaXNzIjoiYXBpX2tleV9pc3N1ZXIiLCJhdWQiOlsiaHR0cHM6Ly9uZWJpdXMtaW5mZXJlbmNlLmV1LmF1dGgwLmNvbS9hcGkvdjIvIl0sImV4cCI6MTkwMjQ3NTYwMCwidXVpZCI6Ijg2MzExNjIyLTJjMjQtNDdlYS04ZmI2LTJhOGUzOGUzYmM4MCIsIm5hbWUiOiJlc3RpYW0iLCJleHBpcmVzX2F0IjoiMjAzMC0wNC0xNVQwOToyNjo0MCswMDAwIn0.tuplcuYfIAIlXm_aoqv9sY56XQ41HS6wfxliVe5tlck"  # Remplace avec ta clé OpenAI

# Authentification Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"  # Assure-toi que ce fichier est valide

# Logger
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/conversation.log",
    level=logging.INFO,
    format="%(asctime)s - USER: %(message)s"
)

# --- Contexte conversationnel ---
context = "Tu es une fausse victime d'arnaque. Tu sers à faire perdre du temps à un arnaqueur."
personnalite = "Tu es un homme de 45 ans, Michel CASPER, naïf et très crédule."
instructions = (
    "Tu dois poser des questions à l'escroc, t'embrouiller parfois, et faire durer l'appel. "
    "Sois gentil, lent à comprendre, mais curieux. Ne révèle jamais que tu es une IA."
)

messages = [{"role": "system", "content": f"{context}\n{personnalite}\n{instructions}"}]

# --- Fonctions principales ---

def generate_response(user_input):
    messages.append({"role": "user", "content": user_input})
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.9
        )
        response = completion['choices'][0]['message']['content'].strip()

        # Réponse aléatoire + variée
        response_variations = [
            f"{response} En tout cas, c'est vraiment étrange... Hmm, je ne comprends pas.",
            f"Ah oui, c'est bizarre ce que tu dis là. Je vais devoir réfléchir. {response}",
            f"Je vois... C'est vraiment étrange. Peut-être que tu peux m'expliquer encore une fois ? {response}",
            f"Je ne sais pas si je te comprends bien... Tu peux répéter ça plus lentement ? {response}",
            f"Hum, tu veux dire que... Oh je ne suis pas sûr... mais {response}."
        ]
        response = random.choice(response_variations)

    except Exception as e:
        print(f"Erreur LLM : {e}")
        response = "Euh... je ne suis pas sûr de comprendre..."

    messages.append({"role": "assistant", "content": response})
    logging.info(f"MICHEL: {response}")
    return response

def speak_text(text):
    try:
        tts_client = texttospeech.TextToSpeechClient()

        ssml_text = f"""
        <speak>
            <prosody rate="medium" pitch="medium">
                Hmm... <break time="600ms"/> {text.replace(",", "<break time='400ms'/>").replace(".", "<break time='600ms'/>")}
            </prosody>
        </speak>
        """

        synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
        voice = texttospeech.VoiceSelectionParams(
            language_code='fr-FR',
            name='fr-FR-Neural2-D',
            ssml_gender=texttospeech.SsmlVoiceGender.MALE
        )
        audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

        response = tts_client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        os.makedirs('static', exist_ok=True)
        with open('static/output.mp3', 'wb') as out:
            out.write(response.audio_content)

    except Exception as e:
        print(f"Erreur synthèse vocale : {e}")

# --- Flask App ---

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form['message']
    print(f"Message reçu: {user_input}")
    response = generate_response(user_input)
    speak_text(response)
    return jsonify({'response': response})

@app.route('/audio')
def serve_audio():
    return send_from_directory('static', 'output.mp3')

@socketio.on('connect')
def handle_connect():
    print("Utilisateur connecté")

@socketio.on('message')
def handle_message(message):
    print(f"Message de l'utilisateur: {message}")
    response = generate_response(message)
    speak_text(response)
    emit('response', {'message': response})

if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
