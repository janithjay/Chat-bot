## Setting Up and Running PizzaBot Chat-bot

Follow these steps to set up and run the PizzaBot chat-bot on your local machine:

1. **Create a Virtual Environment**  
   In the project root directory, run the following command to create a virtual environment:  
   ```bash
   python -m venv venv
   ```

2. **Activate the Virtual Environment**  
   Activate the virtual environment by running:  
   - On Windows:  
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:  
     ```bash
     source venv/bin/activate
     ```

3. **Install Dependencies**  
   Install all required dependencies using the `requirements.txt` file:  
   ```bash
   pip install -r requirements.txt
   ```

4. **Train the Model**  
   Train the Rasa model by executing:  
   ```bash
   rasa train
   ```

5. **Start the Rasa Server**  
   Start the Rasa server with API capabilities enabled:  
   ```bash
   rasa run --enable-api
   ```

6. **Start the Actions Server**  
   Open another terminal and activate the virtual environment, then run the actions server:  
   ```bash
   rasa run actions
   ```

7. **Test the Chatbot Interactively**  
   Use the Rasa shell to test the chatbot:  
   ```bash
   rasa shell
   ```

8. **Finetune the model**
   To fine-tune the model, use the following command:
   ```bash
   python finetune.py
   ```

You can now interact with the PizzaBot chat-bot and test its functionalities!
