## Setting Up and Running PizzaBot Chat-bot

Follow these steps to set up and run the PizzaBot chat-bot on your local machine:

1. **Train the model**  
   In the pizza-bot directory, run the following command to train a model:  
   ```bash
   rasa train
   ```

2. **Start the Rasa Core server**  
   In the pizza-bot directory, run the following command:   
   ```bash
   rasa run -m models --enable-api --cors "*"
   ```

3. **Start the Rasa Action server**  
   In new terminal, in the pizza-bot directory, run the folling command:  
   ```bash
   rasa run actions
   ```
   
4. **Install Tampermonkey chrome extension**   
   Afterwards next commands run in new terminal and inside pizza-bot dirrectory:  
   ```bash
   https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo
   ```

5. **Add new script**  
   After installation click on the extension and follow below steps:  
   ```bash
   rasa train
   ```

6. **Turn on developer mode on browser**  
   Start the Rasa server with API capabilities enabled:  
   ```bash
   rasa run --enable-api
   ```

7. **Start the Actions Server**  
   Open another terminal and activate the virtual environment, then run the actions server:  
   ```bash
   rasa run actions
   ```

8. **Test the Chatbot Interactively**  
   Use the Rasa shell to test the chatbot:  
   ```bash
   rasa shell --port 5006
   ```

8. **Finetune the model**  
   To fine-tune the model, use the following command:  
   ```bash
   python finetune.py
   ```

You can now interact with the PizzaBot chat-bot and test its functionalities!
