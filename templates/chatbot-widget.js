// ==UserScript==
// @name         Pizza Hut LK Chatbot
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Adds chatbot to Pizza Hut Sri Lanka website
// @author       You
// @match        https://www.pizzahut.lk/
// @grant        none
// ==/UserScript==

(function () {
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
            min-width: 300px;
            min-height: 400px;
            max-width: 90vw;
            max-height: 90vh;
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

        #pizza-hut-chatbot .resize-handle {
            position: absolute;
            width: 20px;
            height: 20px;
            top: 0;
            left: 0;
            cursor: nw-resize;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            color: #ffffff;
            z-index: 1000000;
            opacity: 0.7;
            transition: opacity 0.2s;
        }

        #pizza-hut-chatbot .resize-handle:hover {
            opacity: 1;
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
            cursor: move;
            padding-left: 32px; /* Make room for resize handle */
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
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}

        #pizza-hut-chatbot .rw-message {
            padding: 12px 16px !important;
            border-radius: 12px !important;
            max-width: 100% !important;
            margin: 8px 0 !important;
        }

        #pizza-hut-chatbot .rw-client {
            background-color: #f5f5f5 !important;
            color: #1a1a1a !important;
        }

        #pizza-hut-chatbot .rw-response {
            background-color: #ee3124 !important;
            color: white !important;
            float: left !important;
            clear: both !important;
            margin-right: 20% !important;
            font-family: monospace !important;
            white-space: pre !important;
        }

        #pizza-hut-chatbot .rw-message-text {
            margin: 0 !important;
            white-space: pre-wrap !important;
            font-family: monospace !important;
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

        #pizza-hut-chatbot .voice-button {
            background: #ee3124 !important;
    border: none;
    width: 40px !important;
    height: 40px !important;
    border-radius: 50% !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
    padding: 0 !important;
    margin: 0 !important;
        }

        #pizza-hut-chatbot .voice-button:hover {
            opacity: 0.9;
        }

        #pizza-hut-chatbot .voice-button.listening {
            background-color: #ff4433 !important;
    animation: pulse 1.5s infinite;
        }

        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.1); }
            100% { transform: scale(1); }
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
            <div class="resize-handle" id="resizeHandle">⇱</div>
            <div class="chat-header" id="chatHeader">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="background: white; padding: 8px; border-radius: 8px;">
                        <img src="https://i.ibb.co/6P0jH28/logo-pizzahut.png" alt="Pizza Hut Logo" style="width: 205px; height: 32px;">
                    </div>
                    <div>
                        <p></p>
                        <h1 style="font-weight: bold; font-size: 18px;">Virtual Assistant</h1>
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
    const chatHeader = document.getElementById('chatHeader');
    const resizeHandle = document.getElementById('resizeHandle');

    // Resize functionality
    let isResizing = false;
    let isListening = false;
    let originalWidth;
    let originalHeight;
    let originalX;
    let originalY;
    let originalMouseX;
    let originalMouseY;

    resizeHandle.addEventListener('mousedown', initResize);
    document.addEventListener('mousemove', resize);
    document.addEventListener('mouseup', stopResize);

    function initResize(e) {
        isResizing = true;
        originalWidth = chatWindow.offsetWidth;
        originalHeight = chatWindow.offsetHeight;
        originalX = chatWindow.offsetLeft;
        originalY = chatWindow.offsetTop;
        originalMouseX = e.pageX;
        originalMouseY = e.pageY;
    }

    function resize(e) {
        if (!isResizing) return;

        const width = originalWidth + (originalMouseX - e.pageX);
        const height = originalHeight + (originalMouseY - e.pageY);
        const x = originalX - (originalMouseX - e.pageX);
        const y = originalY - (originalMouseY - e.pageY);

        if (width > 300 && width < window.innerWidth * 0.9) {
            chatWindow.style.width = width + 'px';
            chatWindow.style.left = x + 'px';
        }

        if (height > 400 && height < window.innerHeight * 0.9) {
            chatWindow.style.height = height + 'px';
            chatWindow.style.top = y + 'px';
        }
    }

    function stopResize() {
        isResizing = false;
    }

    // Dragging functionality
    let isDragging = false;
    let currentX;
    let currentY;
    let initialX;
    let initialY;
    let xOffset = 0;
    let yOffset = 0;

    chatHeader.addEventListener('mousedown', dragStart);
    document.addEventListener('mousemove', drag);
    document.addEventListener('mouseup', dragEnd);

    function dragStart(e) {
        if (isResizing) return;

        initialX = e.clientX - xOffset;
        initialY = e.clientY - yOffset;

        if (e.target === chatHeader || e.target.parentElement === chatHeader) {
            isDragging = true;
        }
    }

    function drag(e) {
        if (isDragging) {
            e.preventDefault();

            currentX = e.clientX - initialX;
            currentY = e.clientY - initialY;

            xOffset = currentX;
            yOffset = currentY;

            const windowRect = chatWindow.getBoundingClientRect();
            const maxX = window.innerWidth - windowRect.width;
            const maxY = window.innerHeight - windowRect.height;

            currentX = Math.min(Math.max(currentX, 0), maxX);
            currentY = Math.min(Math.max(currentY, 0), maxY);

            setTranslate(currentX, currentY, chatWindow);
        }
    }

    function setTranslate(xPos, yPos, el) {
        el.style.transform = `translate3d(${xPos}px, ${yPos}px, 0)`;
    }

    function dragEnd() {
        initialX = currentX;
        initialY = currentY;
        isDragging = false;
    }

    function handleVoiceCommand() {
        const voiceButton = document.getElementById('voiceButton');
        if (!voiceButton || isListening) return;

        isListening = true;
        voiceButton.classList.add('listening');

        fetch('http://localhost:5000/start_voice', {
            method: 'POST'
        })
            .then(response => response.ok ? response.json() : null)
            .then(data => {
                if (data?.text) {
                    const inputField = document.querySelector('.rw-new-message');
                    if (inputField) {
                        inputField.value = data.text;
                        inputField.dispatchEvent(new KeyboardEvent('keydown', {
                            key: 'Enter',
                            code: 'Enter',
                            keyCode: 13,
                            bubbles: true
                        }));
                    }
                }
            })
            .catch(error => console.error('Voice recognition error:', error))
            .finally(() => {
                isListening = false;
                voiceButton.classList.remove('listening');
            });
    }

    function initializeChat() {
        if (!chatInitialized && window.WebChat) {
            window.WebChat.default(
                {
                    initPayload: '/greet',
                    customData: { language: "en" },
                    socketUrl: "http://localhost:5005", // Replace with your actual Rasa server URL
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
        function addVoiceButton() {
            const sender = document.querySelector('.rw-sender');
            if (sender && !document.getElementById('voiceButton')) {
                const voiceButton = document.createElement('button');
                voiceButton.id = 'voiceButton';
                voiceButton.className = 'voice-button';
                voiceButton.title = 'Voice Command';
                voiceButton.innerHTML = `
                    <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="M12 1a3 3 0 0 0-3 3v8a3 3 0 0 0 6 0V4a3 3 0 0 0-3-3z"></path>
                        <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path>
                        <line x1="12" y1="19" x2="12" y2="23"></line>
                        <line x1="8" y1="23" x2="16" y2="23"></line>
                    </svg>
                `;
                sender.insertBefore(voiceButton, sender.firstChild);

                // Re-attach voice button event listener
                voiceButton.addEventListener('click', handleVoiceCommand);
            }
        }
        setTimeout(addVoiceButton, 1000); // Add delay to ensure Rasa widget is loaded
    }

    // Event listeners
    chatButton.addEventListener('click', function () {
        chatWindow.classList.add('active');
        chatButton.style.display = 'none';
        initializeChat();
    });

    closeChatButton.addEventListener('click', function () {
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