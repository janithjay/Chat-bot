1. Create Virtual Environment
In project root directory
python -m venv venv

2. Activate Virtual Environment
venv\Scripts\activate

3. Install Dependencies
pip install -r requirements.txt

4. Train the model
rasa train

5. Start the Rasa server
rasa run --enable-api

6. In another terminal, start the actions server
rasa run actions

7. Test the chatbot interactively
rasa shell
