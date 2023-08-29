from deepgram import Deepgram
import json
import asyncio
from elevenlabs import generate, play, save, set_api_key
from flask import Flask, request, session, redirect, url_for, send_file
from flask_session import Session
import os
from twilio.twiml.voice_response import Gather, VoiceResponse
from twilio.rest import Client
import openai
import json
from bot import Bot
import requests
from dotenv import load_dotenv
import io
from pydub import AudioSegment

load_dotenv()

DEEPGRAM_API_KEY = 'YOUR_API_KEY'
PATH_TO_FILE = 'male.wav'

account_sid = os.getenv("ACCOUNT_SID")
auth_token = os.getenv("AUTH_TOKEN")
openai.api_key = os.getenv("OPENAI_API_KEY")
set_api_key(os.getenv("ELEVEN_LABS"))

client = Client(account_sid, auth_token)

app = Flask(__name__)
app.secret_key = os.urandom(24)

with open("providers.json", "r") as f:
    providers_data = json.load(f)


def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]


# async def main():
    # deepgram = Deepgram("66288a8974d32bb6254b6b753410422c8759b1c3")
    # Open the audio file
    # with open(PATH_TO_FILE, 'rb') as audio:
    #     # ...or replace mimetype as appropriate
    #     source = {'buffer': audio, 'mimetype': 'audio/wav'}
    #     response = deepgram.transcription.sync_prerecorded(source, {'punctuate': True})
    #     print(json.dumps(response, indent=4))
    # play(audio)

def gather_speech(prompt, session_key, next_action, speechTimeout="auto"):
    generate_audio(prompt)
    response = VoiceResponse()
    # response.say(prompt)
    response.play("https://bfa506899fca.ngrok.app/audio")
    gather = Gather(input='speech', action=next_action,
                    speechTimeout=speechTimeout, speechModel="phone_call")
    response.append(gather)
    if next_action:
        response.redirect(next_action)
    return str(response)


def speech_response(text, next_action=None):
    response = VoiceResponse()
    generate_audio(text)
    response.play("https://bfa506899fca.ngrok.app/audio")
    if next_action:
        response.redirect(next_action)
    return str(response)


def send_sms(msg_body):
    from_number = '+18883395972'
    to_number = request.form.get('From')
    message = client.messages.create(
        body=msg_body,
        from_=from_number,
        to=to_number
    )


def find_provider(caller_response):
    selected_option = caller_response
    options = [
        f"{provider['name']} at {provider['time']}" for provider in providers_data]
    provider_idx = Bot.find_best_match(selected_option, options)
    if provider_idx == 100:
        return None
    else:
        selected_provider = providers_data[provider_idx-1]
        return selected_provider


def generate_audio(prompt):
    audio = generate(
        text=prompt,
        voice="Bella",
        model="eleven_monolingual_v1"
    )
    save(audio, 'test.wav')
    audio = AudioSegment.from_file("test.wav")
    audio = audio.set_frame_rate(8000)
    audio.export("converted.wav", format="wav")


@app.route("/start_call", methods=['GET', 'POST'])
def start_call():
    return gather_speech(
        "Hi, I'm Ruby the AI! Please say your name.",
        "name",
        "/collect_name"
    )


@app.route("/collect_name", methods=['POST'])
def collect_name():
    name = request.form.get("SpeechResult")
    print(name)
    session['name'] = name
    return gather_speech(
        f"Hi, {name}! Pleasure to talk to you. May I know your date of birth please?",
        "dob",
        "/collect_dob"
    )


@app.route("/collect_dob", methods=['POST'])
def collect_dob():
    dob = request.form.get("SpeechResult")
    print(dob)
    session['dob'] = dob
    return gather_speech(
        f"Thank you! What is the reason you are calling in today?",
        "reason",
        "/collect_complaint"
    )


@app.route("/collect_complaint", methods=['POST'])
def collect_complaint():
    complaint = request.form.get("SpeechResult")
    print(complaint)
    session['complaint'] = complaint
    return speech_response(
        "Thank you for sharing that information. Now let me provide you with some available providers and times.",
        "/offer_providers"
    )


@app.route("/offer_providers", methods=['POST'])
def offer_providers():
    # Fake data for demonstration purposes
    options = ", ".join(
        [f"{provider['name']} at {provider['time']}" for provider in providers_data]
    )
    prompt = f"Here are some available options: {options}. Which one do you prefer?"

    return gather_speech(prompt, "selected_provider_time", "/finalize_appointment")


@app.route("/finalize_appointment", methods=['POST'])
def finalize_appointment():
    selected_option = request.form.get("SpeechResult")
    print(selected_option)
    session['selected_provider_time'] = selected_option

    # Match the selected option to the provider data
    # selected_provider = next(
    #     (provider for provider in providers_data if f"{provider['name']} at {provider['time']}" == selected_option),
    #     None
    # )

    selected_provider = find_provider(selected_option)

    if selected_provider:
        session['selected_provider'] = selected_provider
        msg_body = f"Hi {session['name']}, your appointment with {selected_provider['name']} at {selected_provider['time']} has been confirmed. The address is {selected_provider['address']}."
        speech_resp = "Thank you for providing your details. You will receive a confirmation message shortly."
        send_sms(msg_body)
        # Log the session data to a JSON file
        with open("session_log.json", "a") as f:  # "a" means append mode
            json.dump(session, f)
            f.write("\n")
        return speech_response(speech_resp)
    else:
        return speech_response("Sorry, I didn't get that. Please try again.", "/offer_providers")


@app.route("/audio", methods=['GET'])
def audio():
    return send_file("converted.wav", mimetype="audio/wav")


def test_best_match():
    provider = find_provider("Market research")
    print(provider)


if __name__ == "__main__":
    app.run(debug=True)
    # asyncio.run(main())
