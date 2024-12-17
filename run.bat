@echo off
echo Starting Rasa Pizza Chatbot Project

# Activate virtual environment
call venv\Scripts\activate

# Install dependencies (if not already installed)
pip install -r requirements.txt

# Open multiple command prompts
start cmd /k "cd rasa_bot && rasa train"
start cmd /k "cd rasa_bot && rasa run --enable-api"
start cmd /k "python app.py"

echo Project startup initiated
pause