import os
from flask import Flask, render_template, request, jsonify
import requests
import speech_recognition as sr
import pyttsx3

app = Flask(__name__)

# Voice Utility Functions
def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand the audio."
        except sr.RequestError:
            return "Sorry, there was an error with the speech recognition service."

def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Rasa Interaction
def get_rasa_response(message):
    try:
        response = requests.post(
            'http://localhost:5005/webhooks/rest/webhook', 
            json={"sender": "user", "message": message}
        )
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Rasa server: {e}")
        return [{"text": "Sorry, I'm having trouble processing your request."}]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_message = request.json['message']
    rasa_responses = get_rasa_response(user_message)
    
    bot_responses = [
        response.get('text', 'No response') 
        for response in rasa_responses
    ]
    
    # Optional: Text-to-speech for bot responses
    for response in bot_responses:
        text_to_speech(response)
    
    return jsonify({'responses': bot_responses})

@app.route('/voice_input', methods=['POST'])
def voice_input():
    # Convert speech to text
    voice_text = speech_to_text()
    
    # Get Rasa response
    rasa_responses = get_rasa_response(voice_text)
    
    bot_responses = [
        response.get('text', 'No response') 
        for response in rasa_responses
    ]
    
    # Text-to-speech for bot responses
    for response in bot_responses:
        text_to_speech(response)
    
    return jsonify({
        'voice_input': voice_text, 
        'responses': bot_responses
    })

if __name__ == '__main__':
    app.run(debug=True)