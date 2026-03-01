# UMA - Uniting Mothers & Angels

UMA is an AI-powered platform bringing maternal and child healthcare to remote communities in India. The platform features an intelligent chatbot that evaluates patient symptoms and determines severity, automatically connecting patients to medical professionals or emergency services when needed.

## Features

- **AI-Powered Health Assessment**: Instantly analyzes symptoms to detect maternal and child health risks
- **Severity Detection**: Classifies symptoms into four levels (Low, Moderate, High, Critical)
- **Automatic Doctor Connection**: Connects patients to trained medical professionals for high-severity cases
- **Emergency Response**: Automatically dispatches ambulance services for critical conditions
- **Dual Patient Types**: Supports both maternal and child health assessments
- **Modern UI**: Beautiful, accessible design optimized for all devices

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Python Flask
- **AI Model**: Rule-based severity detection system with keyword matching
- **API**: RESTful API endpoints

## Setup Instructions

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- A modern web browser

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "UMA Website"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```
   
   **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start the Flask backend server**
   ```bash
   python app.py
   ```
   
   The API server will start on `http://localhost:5000`

5. **Open the website**
   - Simply open `index.html` in your web browser, or
   - Use a local server (recommended):
     ```bash
     # Using Python's built-in server
     python -m http.server 8000
     ```
     Then navigate to `http://localhost:8000` in your browser

## Project Structure

```
UMA Website/
├── index.html          # Main website HTML
├── style.css           # Website styles
├── script.js           # Website JavaScript (star animation)
├── chatbot.js          # Chatbot JavaScript logic
├── chatbot.css         # Chatbot styles
├── app.py              # Flask backend API server
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── Startup logo.jpeg  # UMA logo
```

## API Endpoints

### POST `/api/chat`
Main chatbot endpoint for processing user messages and detecting severity.

**Request Body:**
```json
{
  "message": "I have severe bleeding",
  "patient_type": "maternal",
  "history": []
}
```

**Response:**
```json
{
  "message": "Response message",
  "severity": "CRITICAL",
  "action": "ambulance",
  "confidence": 0.95,
  "matched_keywords": ["severe bleeding"],
  "timestamp": "2024-01-01T12:00:00"
}
```

### POST `/api/connect-doctor`
Connects patient to a medical professional.

**Request Body:**
```json
{
  "patient_info": {
    "type": "maternal",
    "history": []
  }
}
```

### POST `/api/call-ambulance`
Dispatches ambulance for emergency cases.

**Request Body:**
```json
{
  "patient_info": {
    "type": "maternal",
    "history": []
  },
  "location": "Patient location",
  "symptoms": "Symptom description"
}
```

### GET `/api/health`
Health check endpoint.

## Severity Levels

The AI model classifies symptoms into four severity levels:

1. **LOW**: Mild symptoms, general advice provided
2. **MODERATE**: Symptoms requiring monitoring, doctor consultation suggested
3. **HIGH**: Symptoms requiring immediate medical attention, automatic doctor connection
4. **CRITICAL**: Life-threatening symptoms, automatic ambulance dispatch

## Usage

1. Click the chatbot button (bottom right corner) to open the UMA Health Assistant
2. Select patient type: "Maternal Health" or "Child Health"
3. Describe symptoms or concerns in natural language
4. The AI will analyze and respond with:
   - Severity assessment
   - Recommended action
   - Automatic connection to doctor (if high severity)
   - Automatic ambulance dispatch (if critical)

## Development Notes

- The current implementation uses a rule-based severity detection system
- For production, consider integrating machine learning models for improved accuracy
- Doctor connection and ambulance dispatch are currently simulated
- In production, integrate with actual medical professional APIs and emergency services (108 in India)

## Future Enhancements

- Machine learning model integration for better symptom recognition
- Multi-language support (Hindi, regional languages)
- Voice input/output for accessibility
- Integration with actual medical professional networks
- Real-time location tracking for ambulance dispatch
- Medical history storage and retrieval
- SMS/WhatsApp integration for low-connectivity areas

## Team

- Siddharth Shukla
- Tathagato Chatterjee
- Daraksha Sajid
- Aditya Bakshi
- Pratyush Kumar Rout

## Contact

- Email: teamuma.health@gmail.com
- Instagram: @team_u.m.a

## License

This project is part of a student-led startup initiative.
