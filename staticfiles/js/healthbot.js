class HealthAssistant {
    constructor() {
        this.recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        this.synthesis = window.speechSynthesis;
        this.isListening = false;
        this.setupSpeechRecognition();
    }

    setupSpeechRecognition() {
        this.recognition.continuous = false;
        this.recognition.interimResults = false;
        this.recognition.lang = 'en-US';

        this.recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            this.addUserMessage(transcript);
            this.processUserInput(transcript);
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.toggleListening(false);
        };

        this.recognition.onend = () => {
            if (this.isListening) {
                this.recognition.start();
            }
        };
    }

    toggleListening(force = null) {
        this.isListening = force !== null ? force : !this.isListening;
        const micButton = document.getElementById('mic-button');
        
        if (this.isListening) {
            this.recognition.start();
            micButton.classList.add('listening');
        } else {
            this.recognition.stop();
            micButton.classList.remove('listening');
        }
    }

    async processUserInput(text) {
        try {
            const response = await fetch('/chat/process/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken(),
                },
                body: JSON.stringify({ message: text })
            });

            const data = await response.json();
            
            // Add user message
            this.addUserMessage(text);
            
            // Add symptom analysis if available
            if (data.symptom_analysis && data.symptom_analysis.status === 'success') {
                const analysisMessage = `🔍 Symptom Analysis: ${data.symptom_analysis.condition} (${(data.symptom_analysis.confidence * 100).toFixed(1)}% confidence)`;
                this.addSystemMessage(analysisMessage);
            }
            
            // Add bot response
            this.addBotMessage(data.response);
            this.speak(data.response);
        } catch (error) {
            console.error('Error processing message:', error);
            this.addBotMessage('Sorry, I encountered an error. Please try again.');
        }
    }

    addUserMessage(text) {
        const messagesContainer = document.querySelector('.chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    addBotMessage(text) {
        const messagesContainer = document.querySelector('.chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    addSystemMessage(text) {
        const messagesContainer = document.querySelector('.chat-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system-message';
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    speak(text) {
        if (this.synthesis.speaking) {
            this.synthesis.cancel();
        }

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 1;
        utterance.pitch = 1;
        this.synthesis.speak(utterance);
    }

    getCsrfToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
}

// Initialize the health assistant when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.healthAssistant = new HealthAssistant();
}); 