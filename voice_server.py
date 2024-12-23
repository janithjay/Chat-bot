# voice_server.py
from flask import Flask, jsonify
from flask_cors import CORS
import voice_text  # Import your existing voice_text.py
from voice_text import VoiceBot

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/start_voice', methods=['POST'])
def start_voice():
    try:
        bot = VoiceBot()
        bot.run()
        # Call your voice recognition function from voice_text.py
        recognized_text = voice_text.run()  # Update this to match your actual function name
        return jsonify({'text': recognized_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)
    start_voice()