// ==UserScript==
// @name         Pizza Hut LK Chatbot
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Adds chatbot to Pizza Hut Sri Lanka website
// @author       You
// @match        https://www.pizzahut.lk/
// @grant        none
// ==/UserScript==

(function() {
    // Create a container for our chatbot
    const chatbotContainer = document.createElement('div');
    chatbotContainer.id = 'pizza-hut-chatbot';
    document.body.appendChild(chatbotContainer);

    // Add scoped styles
    const styles = document.createElement('style');
    styles.textContent = `
        #pizza-hut-chatbot .chat-widget-button {
            position: fixed;
            bottom: 24px;
            right: 24px;
            background-color: #ee3124;
            color: white;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            transition: all 0.3s;
            z-index: 999999;
        }

        #pizza-hut-chatbot .chat-widget-button:hover {
            transform: scale(1.1);
        }

        #pizza-hut-chatbot .chat-window {
            position: fixed;
            bottom: 24px;
            right: 24px;
            width: 380px;
            height: 600px;
            max-height: 80vh;
            background: white;
            border-radius: 16px;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.12);
            display: none;
            flex-direction: column;
            overflow: hidden;
            z-index: 999999;
        }

        #pizza-hut-chatbot .chat-window.active {
            display: flex;
        }

        #pizza-hut-chatbot .chat-header {
            background: #ee3124;
            background: linear-gradient(90deg, #ee3124 0%, #c41810 100%);
            padding: 1rem;
            color: white;
            display: flex;
            align-items: center;
            justify-content: space-between;
            flex-shrink: 0;
        }

        #pizza-hut-chatbot .chat-area {
            flex: 1;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            background: #ffffff;
        }

        /* Rasa Widget Overrides */
        #pizza-hut-chatbot .rw-conversation-container {
            box-shadow: none !important;
            border: none !important;
            height: 100% !important;
            max-height: none !important;
            display: flex !important;
            flex-direction: column !important;
        }

        #pizza-hut-chatbot .rw-messages-container {
            padding: 20px !important;
            flex: 1 !important;
            overflow-y: auto !important;
        }

        #pizza-hut-chatbot .rw-sender {
            padding: 16px !important;
            background: white !important;
            border-top: 1px solid rgba(0, 0, 0, 0.1) !important;
        }

        #pizza-hut-chatbot .rw-message {
            padding: 12px 16px !important;
            border-radius: 12px !important;
            max-width: 80% !important;
            margin: 8px 0 !important;
        }

        #pizza-hut-chatbot .rw-client {
            background-color: #f5f5f5 !important;
            color: #1a1a1a !important;
        }

        #pizza-hut-chatbot .rw-response {
            background-color: #ee3124 !important;
            color: white !important;
        }

        #pizza-hut-chatbot .rw-input {
            border-radius: 24px !important;
            padding: 12px 20px !important;
            border: 2px solid #e5e5e5 !important;
        }

        #pizza-hut-chatbot .rw-send {
            background-color: #ee3124 !important;
            border-radius: 50% !important;
            width: 40px !important;
            height: 40px !important;
        }
    `;
    document.head.appendChild(styles);

    // Add chatbot HTML
    chatbotContainer.innerHTML = `
        <div class="chat-widget-button" id="chatButton">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
            </svg>
        </div>
        <div class="chat-window" id="chatWindow">
            <div class="chat-header">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="background: white; padding: 8px; border-radius: 8px;">
                        <img src="https://i.postimg.cc/LXWcT9Dh/logo-pizzahut1.png" alt="Pizza Hut Logo" style="width: 32px; height: 32px;">
                    </div>
                    <div>
                        <h1 style="font-weight: bold; font-size: 18px;">Pizza Hut</h1>
                        <p style="font-size: 14px; opacity: 0.9;">Virtual Assistant</p>
                    </div>
                </div>
                <button id="closeChatButton" style="background: none; border: none; color: white; cursor: pointer;">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </button>
            </div>
            <div class="chat-area" id="chatArea"></div>
        </div>
    `;

    // Initialize chat functionality
    let chatInitialized = false;
    const chatButton = document.getElementById('chatButton');
    const chatWindow = document.getElementById('chatWindow');
    const closeChatButton = document.getElementById('closeChatButton');
    const chatArea = document.getElementById('chatArea');

    function initializeChat() {
        if (!chatInitialized && window.WebChat) {
            window.WebChat.default(
                {
                    initPayload: '/greet',
                    customData: { language: "en" },
                    socketUrl: "http://localhost:5006",  // Replace with your actual Rasa server URL
                    profileAvatar: "https://i.postimg.cc/LXWcT9Dh/logo-pizzahut1.png",
                    params: {
                        images: {
                            dims: {
                                width: 320,
                                height: 240
                            }
                        },
                        storage: "session"
                    },
                    customMessageDelay: (message) => {
                        let delay = message.length * 30;
                        return Math.min(Math.max(delay, 500), 3000);
                    },
                    embedded: true,
                    showCloseButton: false,
                    showFullScreenButton: false,
                    displayUnreadCount: true,
                    onSocketEvent: {
                        'bot_uttered': () => {
                            console.log("Bot responded");
                            scrollToBottom();
                        },
                        'user_uttered': () => {
                            console.log("User sent message");
                            scrollToBottom();
                        },
                        'connect': () => console.log('Connected to bot'),
                        'disconnect': () => console.log('Disconnected from bot')
                    }
                },
                chatArea
            );
            chatInitialized = true;
        }
    }

    // Event listeners
    chatButton.addEventListener('click', function() {
        chatWindow.classList.add('active');
        chatButton.style.display = 'none';
        initializeChat();
    });

    closeChatButton.addEventListener('click', function() {
        chatWindow.classList.remove('active');
        chatButton.style.display = 'flex';
    });

    // Utility functions
    function scrollToBottom() {
        const messagesContainer = document.querySelector('.rw-messages-container');
        if (messagesContainer) {
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        }
    }

    // Load Rasa Web Chat script
    const script = document.createElement('script');
    script.src = "https://cdn.jsdelivr.net/npm/rasa-webchat@1.0.1/lib/index.js";
    script.async = true;
    script.onload = () => {
        console.log('Rasa Web Chat script loaded');
    };
    document.head.appendChild(script);

    // Clear localStorage on initialization
    localStorage.clear();
})();


