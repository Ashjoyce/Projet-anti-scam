                                                                            # L'exécution dans le terminal

from huggingface_hub import InferenceClient
from google.cloud import texttospeech, speech
import os
import sounddevice as sd
import soundfile as sf
import logging
import random

# --- Configuration ---

# Hugging Face LLM client
llm_client = InferenceClient(
    provider="hf-inference",
    api_key="eyJhbGciOiJIUzI1NiIsImtpZCI6IlV6SXJWd1h0dnprLVRvdzlLZWstc0M1akptWXBvX1VaVkxUZlpnMDRlOFUiLCJ0eXAiOiJKV1QifQ.eyJzdWIiOiJnb29nbGUtb2F1dGgyfDExNTYyMDQwMjcwMTg4NDk2NDk1MSIsInNjb3BlIjoib3BlbmlkIG9mZmxpbmVfYWNjZXNzIiwiaXNzIjoiYXBpX2tleV9pc3N1ZXIiLCJhdWQiOlsiaHR0cHM6Ly9uZWJpdXMtaW5mZXJlbmNlLmV1LmF1dGgwLmNvbS9hcGkvdjIvIl0sImV4cCI6MTkwMjQ3NTYwMCwidXVpZCI6Ijg2MzExNjIyLTJjMjQtNDdlYS04ZmI2LTJhOGUzOGUzYmM4MCIsIm5hbWUiOiJlc3RpYW0iLCJleHBpcmVzX2F0IjoiMjAzMC0wNC0xNVQwOToyNjo0MCswMDAwIn0.tuplcuYfIAIlXm_aoqv9sY56XQ41HS6wfxliVe5tlck",
) # il faut remplacer l'API

# Authentification Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "key.json"

# Logger pour enregistrer les conversations
logging.basicConfig(
    filename="logs/conversation.log",
    level=logging.INFO,
    format="%(asctime)s - USER: %(message)s"
)

# --- Contexte conversationnel ---

context = "Tu es une fausse victime d'arnaque. Tu sers à faire perdre du temps à un arnaqueur."
personnalite = "Tu es un homme de 45 ans, Michel CASPER, naïf et très crédule."
instructions = (
    "Tu dois poser des questions à l'escroc, t'embrouiller parfois, et faire durer l'appel."
    " Sois gentil, lent à comprendre, mais curieux. Ne révèle jamais que tu es une IA."
)

messages = [{
    "role": "system",
    "content": f"{context}\n{personnalite}\n{instructions}"
}]

# --- Fonctions principales ---

def record_audio(duration=5, sample_rate=44100):
    print("🎙 Enregistrement...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    print("✅ Enregistrement terminé.")
    sf.write("voice.flac", audio_data, sample_rate)

def transcribe_audio():
    speech_client = speech.SpeechClient()
    with open("voice.flac", "rb") as audio_file:
        content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(sample_rate_hertz=44100, language_code="fr-FR")

    speech_result = speech_client.recognize(config=config, audio=audio)

    if not speech_result.results:
        print("⚠️ Aucune voix détectée.")
        return ""
    transcript = speech_result.results[0].alternatives[0].transcript
    logging.info(f"ARNAQUEUR: {transcript}")
    return transcript

def generate_response(user_input):
    messages.append({"role": "user", "content": user_input})
    
    try:
        completion = llm_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=200,
            temperature=0.9
        )
        response = completion.choices[0].message.content.strip()
        
        # --- Variabilité des réponses ---
        
        # Exemple de randomisation de la longueur de la réponse
        response_variations = [
            f"{response} En tout cas, c'est vraiment étrange... Hmm, je ne comprends pas.",
            f"Ah oui, c'est bizarre ce que tu dis là. Je vais devoir réfléchir. {response}",
            f"Je vois... C'est vraiment étrange. Peut-être que tu peux m'expliquer encore une fois ce que tu veux dire ? {response}",
            f"Je ne sais pas si je te comprends bien... Tu peux répéter ça plus lentement ? {response}",
            f"Hum, tu veux dire que... Oh je ne suis pas sûr... mais {response}."
        ]
        
        # Randomisation dans les réponses pour éviter la répétition
        response = random.choice(response_variations)

    except Exception as e:
        print(f"Erreur LLM : {e}")
        response = "Euh... je ne suis pas sûr de comprendre..."
        
    messages.append({"role": "assistant", "content": response})
    logging.info(f"MICHEL: {response}")
    return response

def speak_text(text):
    tts_client = texttospeech.TextToSpeechClient()

    # Construction SSML avec hésitations et pauses
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

    with open('output.mp3', 'wb') as out:
        out.write(response.audio_content)

    print("🔊 Audio généré avec intonations et pauses.")

# --- Boucle principale ---

if not os.path.exists("logs"):
    os.makedirs("logs")

print("💬 Lancement du piège vocal... Appuyez sur Ctrl+C pour quitter.")

try:
    while True:
        record_audio()
        user_input = transcribe_audio()
        if user_input:
            print("👤 Arnaqueur :", user_input)
            reply = generate_response(user_input)
            print("🤖 Michel :", reply)
            speak_text(reply)
        else:
            print("😐 Silence détecté.")
except KeyboardInterrupt:
    print("\n🛑 Conversation terminée.")
