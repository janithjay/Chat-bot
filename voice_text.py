import requests
import speech_recognition as sr
import pyttsx3
import time
from gtts import gTTS
import os
import pygame

class VoiceBot:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.setup_voice()
        pygame.mixer.init()

    def setup_voice(self):
        """Configure text-to-speech settings"""
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[1].id)  # Index 1 for female voice
        self.engine.setProperty('rate', 150)    # Speed of speech
        self.engine.setProperty('volume', 0.9)  # Volume level

    def speak(self, text):
        """Convert text to speech"""
        try:
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Speech synthesis error: {e}")
            # Fallback to gTTS if pyttsx3 fails
            try:
                tts = gTTS(text=text, lang='en')
                tts.save("response.mp3")
                pygame.mixer.music.load("response.mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    continue
                os.remove("response.mp3")
            except Exception as e:
                print(f"Backup speech synthesis error: {e}")

    def listen(self):
        """Enhanced voice input capture"""
        with sr.Microphone() as source:
            print("Adjusting for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
        
            # Use unique filenames for sound effects
            start_sound = "start_listen.wav"
            end_sound = "end_listen.wav"
        
            if pygame.mixer.get_busy():
                pygame.mixer.stop()
        
            if os.path.exists(start_sound):
                pygame.mixer.Sound(start_sound).play()
        
            print("Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=10)
            
                if pygame.mixer.get_busy():
                    pygame.mixer.stop()
                
                if os.path.exists(end_sound):    
                    pygame.mixer.Sound(end_sound).play()
            
                user_message = self.recognizer.recognize_google(audio)
                print(f"You said: {user_message}")
                return user_message
            
            except sr.UnknownValueError:
                self.speak("Sorry, I couldn't understand that. Could you please repeat?")
            except sr.RequestError as e:
                self.speak("Sorry, there was an error with the speech recognition service.")
                print(f"Request error: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")

    def get_bot_response(self, message):
        """Get response from Rasa server"""
        try:
            response = requests.post(
                'http://localhost:5005/webhooks/rest/webhook', 
                json={"message": message},
                timeout=5
            )
            if response.status_code == 200:
                bot_responses = [item['text'] for item in response.json()]
                if bot_responses:
                    return "\n".join(bot_responses)
                return "I didn't get a response. Please try again."
            else:
                return f"Error: HTTP {response.status_code}"
        except requests.exceptions.Timeout:
            return "The server is taking too long to respond. Please try again."
        except requests.exceptions.ConnectionError:
            return "Unable to connect to the server. Is it running?"
        except Exception as e:
            return f"An error occurred: {e}"

    def run(self):
        """Main loop for the voice bot"""
        self.speak("Hello! I'm Pizza bot. How can I help you?")
        
        while True:
            user_input = self.listen()
            
            if user_input:
                if user_input.lower() in ['exit', 'quit', 'goodbye']:
                    self.speak("Goodbye! Have a great day!")
                    break
                
                response = self.get_bot_response(user_input)
                print(f"Bot: {response}")
                self.speak(response)

if __name__ == "__main__":
    bot = VoiceBot()
    bot.run()