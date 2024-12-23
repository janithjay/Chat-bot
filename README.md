# PizzaBot Chat-bot Setup Guide

This guide will help you set up and run the PizzaBot chat-bot on your local machine. The bot integrates with the PizzaHut.lk website to provide interactive virtual assistance.

## Prerequisites

- Python 3.7 or higher
- Rasa framework installed (`pip install rasa`)
- Chrome browser
- Git (for cloning the repository)

  
Use this command to move into the pizza-bot dirrectory use:
 ```bash
  cd pizza-bot
 ```

## Installation Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/janithjay/Chat-bot
   cd pizza-bot
   ```
   
2. **Install Dependencies**
   Open new terminal, run:
   ```bash
   pip install speechrecognition pyttsx3 gTts pygame pyaudio requests
   ```

3. **Train the Model**
   In the pizza-bot directory, run:
   ```bash
   rasa train
   ```

4. **Start the Rasa Core Server**
   In the pizza-bot directory, run:
   ```bash
   rasa run -m models --enable-api --cors "*" --port 5005
   ```

5. **Start the Rasa Action Server**
   Open a new terminal, navigate to the pizza-bot directory, and run:
   ```bash
   rasa run actions
   ```

6. **Install Tampermonkey Chrome Extension**
   - Visit [Tampermonkey in Chrome Web Store](https://chromewebstore.google.com/detail/tampermonkey/dhdgffkkebhmkfjojejmpbldmpobfkfo)
   - Click "Add to Chrome" and follow the installation prompts

7. **Enable Chrome Developer Mode**
   - Open Chrome settings (⋮)
   - Go to Extensions > Manage extensions
   - Toggle on "Developer mode" in the top right corner

8. **Configure the Chatbot Widget**
   1. Click on the Tampermonkey extension icon
   2. Select "Create a new script"
   3. Copy the content from [`templates/chatbot-widget.js`](https://github.com/janithjay/Chat-bot/blob/bc3dbef39e68cbf705673c05b0bd19f7bf917022/templates/chatbot-widget.js) in your project
   4. Delete the default script content in Tampermonkey
   5. Paste the copied script
   6. Save the script using Ctrl+S or Files > Save
   7. Go to the "Installed Userscripts" tab
   8. Enable the script using the toggle switch

9. **Test the Chatbot**
   - Visit [PizzaHut Sri Lanka](https://www.pizzahut.lk/)
   - The chatbot widget should appear on the page
   - Start interacting with the bot to test its functionality

## Troubleshooting

If you encounter issues:
- Ensure all servers are running (Rasa Core and Action servers)
- Check the browser console for any JavaScript errors
- Verify that the Tampermonkey script is enabled
- Confirm that the CORS settings are correct in the Rasa server
