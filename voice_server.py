from flask import Flask, jsonify, request
from flask_cors import CORS
from gtts import gTTS
import pygame
from voice_text import VoiceBot
import threading
import requests
import time
import os

app = Flask(__name__)
CORS(app)

class EnhancedVoiceBot(VoiceBot):
    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        
    def get_bot_response(self, message):
        """Enhanced get_bot_response with better error handling"""
        try:
            # Increase timeout to 10 seconds
            response = requests.post(
                'http://localhost:5005/webhooks/rest/webhook', 
                json={"message": message},
                timeout=10  # Increased timeout
            )
            
            # Add debug logging
            print(f"Rasa server response status: {response.status_code}")
            print(f"Rasa server response: {response.text}")
            
            if response.status_code == 200:
                bot_responses = [item['text'] for item in response.json()]
                if bot_responses:
                    return "\n".join(bot_responses)
                return "I didn't understand that. Could you please rephrase?"
            else:
                print(f"Rasa server error: {response.status_code}")
                return "I'm having trouble understanding right now. Please try again."
                
        except requests.exceptions.Timeout:
            print("Rasa server timeout")
            return "I'm taking too long to process. Please try again in a moment."
        except requests.exceptions.ConnectionError:
            print("Rasa server connection error")
            return "I'm having trouble connecting to my brain. Is the Rasa server running?"
        except Exception as e:
            print(f"Unexpected error in get_bot_response: {str(e)}")
            return "I encountered an unexpected error. Please try again."

    def safe_speak(self, text):
        """Thread-safe speaking with better error handling"""
        with self._lock:
            try:
                # Add retry logic for file cleanup
                max_retries = 3
                for _ in range(max_retries):
                    try:
                        if os.path.exists("response.mp3"):
                            os.remove("response.mp3")
                            time.sleep(0.2)  # Increased delay
                        break
                    except OSError:
                        time.sleep(0.5)  # Wait longer between retries
            
                # Use unique filenames for concurrent requests
                timestamp = str(int(time.time() * 1000))
                filename = f"response_{timestamp}.mp3"
            
                tts = gTTS(text=text, lang='en')
                tts.save(filename)
            
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                
            except Exception as e:
                print(f"Speech error: {e}")
            finally:
                try:
                    if os.path.exists(filename):
                        pygame.mixer.music.unload()
                        time.sleep(0.1)
                        os.remove(filename)
                except:
                    pass

@app.route('/start_voice', methods=['POST'])
def start_voice():
    try:
        bot = EnhancedVoiceBot()
        recognized_text = bot.listen()
        
        if recognized_text:
            print(f"Recognized text: {recognized_text}")
            
            # Get bot response
            bot_response = bot.get_bot_response(recognized_text)
            print(f"Bot response: {bot_response}")
            
            # Return both texts immediately
            response_data = {
                'input_text': recognized_text,
                'bot_response': bot_response
            }
            
            # Handle speech in separate thread
            threading.Thread(target=bot.safe_speak, args=(bot_response,)).start()
            
            return jsonify(response_data)
        else:
            return jsonify({
                'error': 'No speech detected'
            }), 400
            
    except Exception as e:
        print(f"Server error in start_voice: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/get_response', methods=['POST'])
def get_response():
    try:
        message = request.json.get('message', '')
        bot = EnhancedVoiceBot()
        response = bot.get_bot_response(message)
        return jsonify({'response': response})
    except Exception as e:
        print(f"Error in get_response: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000)