class HealthAssistant {
    constructor() {
        // Initialize speech recognition
        if ('webkitSpeechRecognition' in window) {
            this.recognition = new webkitSpeechRecognition();
            this.setupSpeechRecognition();
        } else {
            console.warn('Speech recognition not supported in this browser');
        }

        // Initialize speech synthesis
        if ('speechSynthesis' in window) {
        this.synthesis = window.speechSynthesis;
        } else {
            console.warn('Speech synthesis not supported in this browser');
        }

        // Get DOM elements
        this.micButton = document.getElementById('mic-button');
        this.chatInput = document.querySelector('.chat-input input');
        this.chatMessages = document.querySelector('.chat-messages');
        this.sendButton = document.querySelector('.chat-input button[type="submit"]');

        // Bind event listeners
        this.micButton?.addEventListener('click', () => this.toggleListening());
        this.sendButton?.addEventListener('click', (e) => {
            e.preventDefault();
            this.processUserInput();
        });
        this.chatInput?.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.processUserInput();
            }
        });

        // Initialize with welcome message
        this.addSystemMessage("Welcome to E-Swasthya+! I'm here to help you with our healthcare platform.");
    }

    setupSpeechRecognition() {
        this.recognition.continuous = false;
        this.recognition.interimResults = true;
        this.recognition.lang = 'en-US';

        this.recognition.onstart = () => {
            this.micButton.classList.add('listening');
            this.addSystemMessage('Listening...');
        };

        this.recognition.onend = () => {
            this.micButton.classList.remove('listening');
            this.removeSystemMessage('Listening...');
        };

        this.recognition.onresult = (event) => {
            const result = event.results[0];
            if (result.isFinal) {
                this.chatInput.value = result[0].transcript;
                this.processUserInput();
            } else {
                this.showInterimResult(result[0].transcript);
            }
        };

        this.recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            this.addSystemMessage('Error: ' + event.error);
            this.micButton.classList.remove('listening');
        };
    }

    toggleListening() {
        if (this.micButton.classList.contains('listening')) {
            this.recognition.stop();
        } else {
            this.recognition.start();
        }
    }

    showInterimResult(text) {
        const interimDiv = document.querySelector('.interim-result') || document.createElement('div');
        interimDiv.className = 'interim-result message';
        interimDiv.textContent = text;
        
        if (!document.querySelector('.interim-result')) {
            this.chatMessages.appendChild(interimDiv);
        }
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    async processUserInput() {
        const userInput = this.chatInput.value.trim();
        if (!userInput) return;

        // Add user message to chat
        this.addUserMessage(userInput);
        this.chatInput.value = '';

        try {
            const response = await fetch('/chat/process/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ message: userInput })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            
            if (data.status === 'error') {
                throw new Error(data.message || 'Unknown error occurred');
            }

            // Handle symptom analysis if available
            if (data.symptom_analysis && data.symptom_analysis.analysis) {
                const analysis = data.symptom_analysis.analysis;
                let analysisMessage = '🔍 Symptom Analysis:\n';
                
                // Add identified symptoms
                if (analysis.identified_symptoms.length > 0) {
                    analysisMessage += '\nIdentified Symptoms:\n';
                    analysis.identified_symptoms.forEach(symptom => {
                        analysisMessage += `• ${symptom.symptom} (Severity: ${symptom.severity})\n`;
                    });
                }
                
                // Add possible conditions
                if (analysis.possible_conditions.length > 0) {
                    analysisMessage += '\nPossible Conditions:\n';
                    analysis.possible_conditions.forEach(condition => {
                        analysisMessage += `• ${condition}\n`;
                    });
                }
                
                // Add recommended action
                analysisMessage += `\nRecommended Action: ${analysis.recommended_action}`;
                
                // Add additional notes if available
                if (analysis.additional_notes) {
                    analysisMessage += `\n\nNote: ${analysis.additional_notes}`;
                }
                
                this.addSystemMessage(analysisMessage);
            }

            // Add bot response
            if (data.response) {
                const botMessage = this.addBotMessage(data.response);
                this.speak(data.response, botMessage);
            }

        } catch (error) {
            console.error('Error:', error);
            this.addSystemMessage('Sorry, there was an error processing your request: ' + error.message);
        }
    }

    addUserMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.textContent = text;
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    addBotMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.textContent = text;
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
        return messageDiv;
    }

    addSystemMessage(text) {
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system-message';
        messageDiv.textContent = text;
        this.chatMessages.appendChild(messageDiv);
        this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
    }

    removeSystemMessage(text) {
        const systemMessages = this.chatMessages.querySelectorAll('.system-message');
        systemMessages.forEach(msg => {
            if (msg.textContent === text) {
                msg.remove();
            }
        });
    }

    speak(text, messageElement) {
        if (!this.synthesis) return;

        // Cancel any ongoing speech
        this.synthesis.cancel();

        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'en-US';
        utterance.rate = 1;
        utterance.pitch = 1;

        utterance.onstart = () => {
            messageElement.classList.add('speaking');
        };

        utterance.onend = () => {
            messageElement.classList.remove('speaking');
        };

        this.synthesis.speak(utterance);
    }

    getCsrfToken() {
        const csrfCookie = document.cookie.split(';')
            .find(cookie => cookie.trim().startsWith('csrftoken='));
        if (csrfCookie) {
            return csrfCookie.split('=')[1];
        }
        const csrfInput = document.querySelector('[name="csrfmiddlewaretoken"]');
        return csrfInput ? csrfInput.value : '';
    }
}

// Initialize the health assistant when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.healthAssistant = new HealthAssistant();
}); 