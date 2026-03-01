# UMA - Uniting Mothers & Angels (MERN Stack)

UMA is an AI-powered platform bringing maternal and child healthcare to remote communities in India. The platform features an intelligent chatbot that evaluates patient symptoms and determines severity, automatically connecting patients to medical professionals or emergency services when needed.

## Tech Stack

- **Frontend**: React.js
- **Backend**: Node.js + Express.js
- **Database**: MongoDB
- **AI**: Rule-based severity detection system with keyword matching

## Project Structure

```
UMA Website/
├── backend/
│   ├── models/
│   │   └── Conversation.js      # MongoDB schema for conversations
│   ├── routes/
│   │   ├── chat.js             # Chat API endpoint
│   │   ├── doctor.js           # Doctor connection endpoint
│   │   └── ambulance.js         # Ambulance dispatch endpoint
│   ├── services/
│   │   └── severityDetector.js  # AI severity detection logic
│   ├── server.js               # Express server setup
│   ├── package.json
│   └── .env.example
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.js
│   │   │   ├── Home.js
│   │   │   ├── About.js
│   │   │   ├── Features.js
│   │   │   ├── Team.js
│   │   │   ├── Contact.js
│   │   │   └── Chatbot.js      # Main chatbot component
│   │   ├── App.js
│   │   └── index.js
│   └── package.json
└── README_MERN.md
```

## Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- MongoDB (local installation or MongoDB Atlas account)

## Installation & Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Install dependencies
npm install

# Create .env file (copy from .env.example)
# For local MongoDB:
# MONGODB_URI=mongodb://localhost:27017/uma-health
# PORT=5000

# Start the backend server
npm start

# Or for development with auto-reload:
npm run dev
```

The backend server will run on `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the React development server
npm start
```

The frontend will run on `http://localhost:3000` and automatically open in your browser.

### 3. MongoDB Setup

#### Option A: Local MongoDB

1. Install MongoDB from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Start MongoDB service:
   ```bash
   # Windows
   net start MongoDB
   
   # macOS/Linux
   sudo systemctl start mongod
   ```
3. Use connection string: `mongodb://localhost:27017/uma-health`

#### Option B: MongoDB Atlas (Cloud)

1. Create a free account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a new cluster
3. Get your connection string
4. Update `MONGODB_URI` in `backend/.env`

## API Endpoints

### POST `/api/chat`
Main chatbot endpoint for processing user messages and detecting severity.

**Request Body:**
```json
{
  "message": "I have severe bleeding",
  "patient_type": "maternal",
  "history": [],
  "conversation_id": "optional_conversation_id"
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
  "timestamp": "2024-01-01T12:00:00",
  "conversation_id": "conversation_id"
}
```

### POST `/api/connect-doctor`
Connects patient to a medical professional.

**Request Body:**
```json
{
  "patient_info": {
    "type": "maternal"
  },
  "conversation_id": "optional_conversation_id"
}
```

### POST `/api/call-ambulance`
Dispatches ambulance for emergency cases.

**Request Body:**
```json
{
  "patient_info": {
    "type": "maternal"
  },
  "location": "Patient location",
  "symptoms": "Symptom description",
  "conversation_id": "optional_conversation_id"
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

## Features

- ✅ AI-Powered Health Assessment
- ✅ Severity Detection (LOW, MODERATE, HIGH, CRITICAL)
- ✅ Automatic Doctor Connection (for HIGH severity)
- ✅ Automatic Ambulance Dispatch (for CRITICAL severity)
- ✅ Dual Patient Types (Maternal & Child Health)
- ✅ Conversation History Storage (MongoDB)
- ✅ Modern, Responsive UI
- ✅ Real-time Chat Interface

## Usage

1. Start both backend and frontend servers
2. Open the website in your browser (`http://localhost:3000`)
3. Click the chatbot button (bottom right corner)
4. Select patient type: "Maternal Health" or "Child Health"
5. Describe symptoms or concerns in natural language
6. The AI will analyze and respond with:
   - Severity assessment
   - Recommended action
   - Automatic connection to doctor (if high severity)
   - Automatic ambulance dispatch (if critical)

## Development

### Backend Development
```bash
cd backend
npm run dev  # Uses nodemon for auto-reload
```

### Frontend Development
```bash
cd frontend
npm start  # React development server with hot reload
```

### Building for Production

**Frontend:**
```bash
cd frontend
npm run build
```

**Backend:**
```bash
cd backend
npm start
```

## Environment Variables

### Backend (.env)
```
MONGODB_URI=mongodb://localhost:27017/uma-health
PORT=5000
NODE_ENV=development
```

### Frontend
Create `.env` file in frontend directory:
```
REACT_APP_API_URL=http://localhost:5000/api
```

## Future Enhancements

- Machine learning model integration for better symptom recognition
- Multi-language support (Hindi, regional languages)
- Voice input/output for accessibility
- Integration with actual medical professional networks
- Real-time location tracking for ambulance dispatch
- SMS/WhatsApp integration for low-connectivity areas
- User authentication and patient profiles
- Medical history dashboard

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
