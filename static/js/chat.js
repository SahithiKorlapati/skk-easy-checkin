document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const chatWidget = document.getElementById('chat-widget');
    const chatToggle = document.getElementById('chat-toggle');
    const minimizeChat = document.getElementById('minimize-chat');
    const closeChat = document.getElementById('close-chat');
    const chatInput = document.getElementById('chat-input');
    const chatMessages = document.getElementById('chat-messages');
    const sendButton = document.getElementById('send-message');
    const emojiButton = document.getElementById('emoji-button');
    
    // State
    let isTyping = false;
    let isMinimized = false;
    let messageHistory = [];
    
    // Initialize chat
    function initChat() {
        // Show welcome message if first visit
        const welcomeMessage = {
            text: "Hello! I'm your AI assistant. How can I help you today?",
            sender: 'bot',
            timestamp: new Date()
        };
        
        // Add welcome message to history and display
        messageHistory.push(welcomeMessage);
        displayMessage(welcomeMessage);
        
        // Make chat widget visible with animation
        setTimeout(() => {
            chatWidget.classList.add('visible');
        }, 500);
    }
    
    // Toggle chat widget
    function toggleChat() {
        if (isMinimized) {
            // Restore from minimized
            chatWidget.style.height = '600px';
            chatWidget.style.width = '380px';
            chatWidget.style.borderRadius = '12px';
            chatMessages.style.display = 'flex';
            document.querySelector('.chat-input-container').style.display = 'flex';
            isMinimized = false;
        } else {
            // Toggle visibility
            if (chatWidget.classList.contains('visible')) {
                chatWidget.classList.remove('visible');
                chatToggle.style.transform = 'scale(1)';
            } else {
                chatWidget.classList.add('visible');
                chatInput.focus();
            }
        }
    }
    
    // Minimize chat to just the header
    function minimizeChatWindow() {
        chatWidget.style.height = '60px';
        chatWidget.style.width = '300px';
        chatWidget.style.borderRadius = '30px';
        chatMessages.style.display = 'none';
        document.querySelector('.chat-input-container').style.display = 'none';
        isMinimized = true;
    }
    
    // Add a new message to the chat
    function addMessage(text, sender) {
        const message = {
            text: text,
            sender: sender,
            timestamp: new Date()
        };
        
        // Add to history
        messageHistory.push(message);
        
        // Display the message
        displayMessage(message);
        
        // If it's a user message, get a response
        if (sender === 'user') {
            getAIResponse(text);
        }
    }
    
    // Display a message in the chat
    function displayMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = `chat-message ${message.sender}-message`;
        
        // Add timestamp
        const timeString = message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
        
        // Create message HTML
        messageElement.innerHTML = `
            <div class="message-content">${message.text}</div>
            <div class="message-time">${timeString}</div>
        `;
        
        // Add to chat
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Show typing indicator
    function showTypingIndicator() {
        if (document.querySelector('.typing-indicator')) return;
        
        const typingElement = document.createElement('div');
        typingElement.className = 'typing-indicator';
        typingElement.innerHTML = `
            <span></span>
            <span></span>
            <span></span>
        `;
        
        chatMessages.appendChild(typingElement);
        scrollToBottom();
        
        return typingElement;
    }
    
    // Remove typing indicator
    function removeTypingIndicator() {
        const typingElement = document.querySelector('.typing-indicator');
        if (typingElement) {
            typingElement.remove();
        }
    }
    
    // Get AI response
    function getAIResponse(userMessage) {
        if (isTyping) return;
        
        isTyping = true;
        const typingIndicator = showTypingIndicator();
        
        // Call OpenAI API
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                message: userMessage,
                history: messageHistory.slice(-4) // Send last 4 messages for context
            })
        })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator();
            isTyping = false;
            
            if (data.response) {
                addMessage(data.response, 'bot');
            } else {
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            removeTypingIndicator();
            isTyping = false;
            addMessage('Error connecting to the AI service. Please try again later.', 'bot');
        });
    }
    
    // Scroll chat to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Send message handler
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message === '' || isTyping) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        chatInput.value = '';
        
        // Keep focus on input
        chatInput.focus();
    }
    
    // Event Listeners
    chatToggle.addEventListener('click', toggleChat);
    minimizeChat.addEventListener('click', minimizeChatWindow);
    closeChat.addEventListener('click', () => chatWidget.classList.remove('visible'));
    
    sendButton.addEventListener('click', sendMessage);
    
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    // Emoji picker (placeholder - would need an emoji picker library)
    emojiButton.addEventListener('click', function() {
        // This would open an emoji picker in a real implementation
        chatInput.focus();
    });
    
    // Handle click outside to close chat
    document.addEventListener('click', function(event) {
        if (!chatWidget.contains(event.target) && event.target !== chatToggle) {
            if (!chatWidget.contains(event.target)) {
                chatWidget.classList.remove('visible');
            }
        }
    });
    
    // Initialize the chat
    initChat();
});
