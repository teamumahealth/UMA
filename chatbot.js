class UMAChatbot {
    constructor() {
        this.apiUrl = 'http://localhost:5000/api';
        this.isOpen = false;
        this.conversationHistory = [];
        this.patientType = 'maternal';
        this.init();
    }

    init() {
        this.createChatbotUI();
        this.attachEventListeners();
        this.addWelcomeMessage();
    }

    createChatbotUI() {
        const chatbotHTML = `
            <div id="uma-chatbot-container">
                <div id="uma-chatbot-header">
                    <div class="chatbot-title-section">
                         <img src="Startup logo.jpeg" alt="UMA Logo" class="chatbot-logo">
                         <div class="chatbot-title">
                            <h3>UMA</h3>
                            <span class="chatbot-status">AI Powered</span>
                        </div>
                    </div>
                    <button id="uma-chatbot-minimize" class="chatbot-btn-minimize">−</button>
                </div>
                <div id="uma-chatbot-body">
                    <div id="uma-chatbot-messages"></div>
                    <div id="uma-chatbot-actions" style="display: none;">
                        <button id="btn-connect-doctor" class="action-btn">Connect to Doctor</button>
                        <button id="btn-call-ambulance" class="action-btn emergency">Call Ambulance</button>
                    </div>
                </div>
                <div id="uma-chatbot-input-area">
                    <div class="patient-type-selector">
                        <label>Patient Type:</label>
                        <select id="patient-type-select">
                            <option value="maternal">Maternal Health</option>
                            <option value="child">Child Health</option>
                        </select>
                    </div>
                    <div class="input-wrapper">
                        <input type="text" id="uma-chatbot-input" placeholder="Describe your symptoms or concerns..." />
                        <button id="uma-chatbot-send">Send</button>
                    </div>
                </div>
            </div>
            <button id="uma-chatbot-toggle" class="chatbot-toggle-btn">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M20 2H4C2.9 2 2 2.9 2 4V22L6 18H20C21.1 18 22 17.1 22 16V4C22 2.9 21.1 2 20 2Z" fill="white"/>
                </svg>
            </button>
        `;
        document.body.insertAdjacentHTML('beforeend', chatbotHTML);
    }

    attachEventListeners() {
        document.getElementById('uma-chatbot-toggle').addEventListener('click', () => this.toggleChatbot());
        document.getElementById('uma-chatbot-minimize').addEventListener('click', () => this.toggleChatbot());

        const sendBtn = document.getElementById('uma-chatbot-send');
        const input = document.getElementById('uma-chatbot-input');

        sendBtn.addEventListener('click', () => this.sendMessage());
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') this.sendMessage();
        });

        document.getElementById('patient-type-select').addEventListener('change', (e) => {
            this.patientType = e.target.value;
        });

        document.getElementById('btn-connect-doctor').addEventListener('click', () => this.connectDoctor());
        document.getElementById('btn-call-ambulance').addEventListener('click', () => this.callAmbulance());
    }

    toggleChatbot() {
        this.isOpen = !this.isOpen;
        const container = document.getElementById('uma-chatbot-container');
        const toggleBtn = document.getElementById('uma-chatbot-toggle');

        if (this.isOpen) {
            container.classList.add('open');
            toggleBtn.style.display = 'none';
            document.getElementById('uma-chatbot-input').focus();
        } else {
            container.classList.remove('open');
            toggleBtn.style.display = 'flex';
        }
    }

    addWelcomeMessage() {
        const welcomeMsg = {
            type: 'bot',
            message: 'Hello! I\'m UMA, your AI-powered health assistant. 🤖 I\'m trained on comprehensive health data and use generative AI to provide intelligent responses about maternal and child health concerns. Please describe any symptoms or concerns you have, and I\'ll help determine the severity and connect you with appropriate care.',
            timestamp: new Date()
        };
        this.addMessageToChat(welcomeMsg);
    }

    async sendMessage() {
        const input = document.getElementById('uma-chatbot-input');
        const message = input.value.trim();

        if (!message) return;

        const userMsg = {
            type: 'user',
            message: message,
            timestamp: new Date()
        };
        this.addMessageToChat(userMsg);
        this.conversationHistory.push({ role: 'user', content: message });

        input.value = '';
        this.showTypingIndicator();

        try {
            const response = await fetch(`${this.apiUrl}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    message: message,
                    patient_type: this.patientType,
                    history: this.conversationHistory,
                    use_ai: true  // Enable generative AI responses
                })
            });

            const data = await response.json();
            this.hideTypingIndicator();

            // Add AI badge if response was AI-generated
            let messageContent = data.message;
            if (data.response_type === 'ai_generated') {
                messageContent = `🤖 <small style="color: #888; font-size: 0.8em;">AI-Powered Response</small><br>${data.message}`;
            }

            const botMsg = {
                type: 'bot',
                message: messageContent,
                severity: data.severity,
                action: data.action,
                response_type: data.response_type,
                timestamp: new Date()
            };
            this.addMessageToChat(botMsg);
            this.conversationHistory.push({ role: 'assistant', content: data.message });

            this.handleSeverityAction(data.severity, data.action);

        } catch (error) {
            console.error('Error:', error);
            this.hideTypingIndicator();
            this.addMessageToChat({
                type: 'bot',
                message: 'I apologize, but I\'m having trouble connecting to the server. Please ensure the backend API is running. In a production environment, this would be automatically handled.',
                timestamp: new Date()
            });
        }
    }

    handleSeverityAction(severity, action) {
        const actionsDiv = document.getElementById('uma-chatbot-actions');
        const connectBtn = document.getElementById('btn-connect-doctor');
        const ambulanceBtn = document.getElementById('btn-call-ambulance');

        if (severity === 'CRITICAL') {
            actionsDiv.style.display = 'flex';
            ambulanceBtn.style.display = 'block';
            connectBtn.style.display = 'none';
            setTimeout(() => this.callAmbulance(), 500);
        } else if (severity === 'HIGH') {
            actionsDiv.style.display = 'flex';
            connectBtn.style.display = 'block';
            ambulanceBtn.style.display = 'none';
            setTimeout(() => this.connectDoctor(), 500);
        } else if (action === 'suggest_doctor') {
            actionsDiv.style.display = 'flex';
            connectBtn.style.display = 'block';
            ambulanceBtn.style.display = 'none';
        } else {
            actionsDiv.style.display = 'none';
        }
    }

    async connectDoctor() {
        this.addMessageToChat({
            type: 'system',
            message: 'Connecting you to a medical professional...',
            timestamp: new Date()
        });

        try {
            const response = await fetch(`${this.apiUrl}/connect-doctor`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    patient_info: {
                        type: this.patientType,
                        history: this.conversationHistory
                    }
                })
            });

            const data = await response.json();

            this.addMessageToChat({
                type: 'bot',
                message: data.message,
                timestamp: new Date()
            });

            if (data.doctor) {
                this.addMessageToChat({
                    type: 'system',
                    message: `Doctor: ${data.doctor.name} | Specialization: ${data.doctor.specialization} | Experience: ${data.doctor.experience}`,
                    timestamp: new Date()
                });
            }

        } catch (error) {
            console.error('Error connecting to doctor:', error);
            this.addMessageToChat({
                type: 'bot',
                message: 'Unable to connect to doctor service. In production, this would automatically connect to a medical professional.',
                timestamp: new Date()
            });
        }

        document.getElementById('uma-chatbot-actions').style.display = 'none';
    }

    async callAmbulance() {
        this.addMessageToChat({
            type: 'system',
            message: '🚨 Emergency services are being notified...',
            timestamp: new Date()
        });

        try {
            const response = await fetch(`${this.apiUrl}/call-ambulance`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    patient_info: {
                        type: this.patientType,
                        history: this.conversationHistory
                    },
                    location: 'Location not provided',
                    symptoms: this.conversationHistory.map(h => h.content).join(' ')
                })
            });

            const data = await response.json();

            this.addMessageToChat({
                type: 'bot',
                message: data.message,
                timestamp: new Date()
            });

            if (data.ambulance) {
                this.addMessageToChat({
                    type: 'system',
                    message: `Ambulance ID: ${data.ambulance.ambulance_id} | ETA: ${data.ambulance.estimated_arrival}`,
                    timestamp: new Date()
                });
            }

        } catch (error) {
            console.error('Error calling ambulance:', error);
            this.addMessageToChat({
                type: 'bot',
                message: 'Unable to connect to emergency services. In production, this would automatically dispatch an ambulance. Please call 108 or your local emergency number immediately!',
                timestamp: new Date()
            });
        }

        document.getElementById('uma-chatbot-actions').style.display = 'none';
    }

    addMessageToChat(messageObj) {
        const messagesDiv = document.getElementById('uma-chatbot-messages');
        const messageElement = document.createElement('div');
        messageElement.className = `chatbot-message ${messageObj.type}`;

        const time = messageObj.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

        messageElement.innerHTML = `
            <div class="message-content">${this.formatMessage(messageObj.message)}</div>
            <div class="message-time">${time}</div>
        `;

        messagesDiv.appendChild(messageElement);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    formatMessage(message) {
        return message.replace(/\n/g, '<br>');
    }

    showTypingIndicator() {
        const messagesDiv = document.getElementById('uma-chatbot-messages');
        const typingDiv = document.createElement('div');
        typingDiv.id = 'typing-indicator';
        typingDiv.className = 'chatbot-message bot';
        typingDiv.innerHTML = `
            <div class="message-content typing">
                <span></span><span></span><span></span>
            </div>
        `;
        messagesDiv.appendChild(typingDiv);
        messagesDiv.scrollTop = messagesDiv.scrollHeight;
    }

    hideTypingIndicator() {
        const typingDiv = document.getElementById('typing-indicator');
        if (typingDiv) {
            typingDiv.remove();
        }
    }
}

document.addEventListener('DOMContentLoaded', () => {
    window.umaChatbot = new UMAChatbot();
});
