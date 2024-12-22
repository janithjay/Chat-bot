import requests
import speech_recognition as sr  # Import library for speech recognition

def get_bot_response(message):
    """
    Sends the user message to the Rasa server and gets the bot's response.
    """
    try:
        response = requests.post('http://localhost:5055/webhooks/rest/webhook', json={"message": message})
        if response.status_code == 200:
            bot_responses = [item['text'] for item in response.json()]
            return "\n".join(bot_responses)
        else:
            return "Error: Unable to connect to the bot. Please check the Rasa server."
    except Exception as e:
        return f"Exception occurred: {e}"


def voice_to_text():
    """
    Captures voice input from the user and converts it to text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything: ")
        try:
            audio = recognizer.listen(source)
            user_message = recognizer.recognize_google(audio)
            print(f"You said: {user_message}")
            return user_message
        except sr.UnknownValueError:
            print("Sorry, I could not understand your speech.")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
    return None


def main():
    print("Welcome to PizzaBot! (Type 'exit' to quit)")
    print("You can either type your message or speak it (if you want to use voice input, just press Enter without typing anything).")

    while True:
        user_input = input("Your input (or press Enter for voice input): ").strip()

        # If the user chooses voice input
        if not user_input:
            print("Switching to voice input...")
            user_input = voice_to_text()

        # If the user chooses to exit or there's no valid input
        if user_input is None:
            print("No input detected. Please try again.")
            continue
        if user_input.lower() == 'exit':
            print("Goodbye! Thanks for using PizzaBot.")
            break

        # Get bot response
        bot_response = get_bot_response(user_input)
        print(f"Bot says: {bot_response}")


if __name__ == "__main__":
    main()
