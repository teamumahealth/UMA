# UMA AI Chatbot - Generative AI Training Setup Guide

## Overview
This guide will help you set up the UMA chatbot with **generative AI capabilities** powered by OpenAI and trained on health data from GitHub.

## Features Implemented

### 1. **GitHub Health Data Integration**
The chatbot now has a comprehensive knowledge base with data on:
- **Maternal Health**: Pregnancy complications, nutrition, prenatal care
- **Child Health**: Common illnesses, immunization schedules, child safety

### 2. **Generative AI Responses**
Using OpenAI's GPT-3.5-turbo, the chatbot generates intelligent, context-aware responses rather than just pattern matching.

### 3. **Enhanced Context Awareness**
- Conversation history tracking
- Patient type-specific responses
- Severity-level adjusted recommendations
- Knowledge base integration

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**New packages added:**
- `openai==1.3.0` - OpenAI API client
- `requests==2.31.0` - HTTP requests
- `python-dotenv==1.0.0` - Environment variable management
- `PyGithub==2.1.1` - GitHub API integration

### Step 2: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com)
2. Sign up or log in to your account
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key (it will only be shown once)

### Step 3: Configure Environment Variables

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Edit `.env` and add your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

### Step 4: Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## How It Works

### Knowledge Base Structure
```
GITHUB_HEALTH_DATA
├── maternal
│   ├── pregnancy_complications
│   ├── nutrition
│   └── prenatal_care
└── child
    ├── common_illnesses
    ├── immunization
    └── child_safety
```

### Response Generation Flow

```
User Message
    ↓
Severity Detection (keyword matching)
    ↓
AI Response Generation (if OpenAI available)
    ├─→ Build context from knowledge base
    ├─→ Include conversation history
    ├─→ Call OpenAI GPT-3.5-turbo
    └─→ Return AI-generated response
    ↓
Action Determination (doctor/ambulance based on severity)
    ↓
Response to User
```

## API Endpoints

### POST `/api/chat`
Generate chatbot response with AI capabilities

**Request:**
```json
{
  "message": "I have a severe headache",
  "patient_type": "maternal",
  "history": [],
  "use_ai": true
}
```

**Response:**
```json
{
  "message": "Based on your symptoms...",
  "action": "doctor",
  "severity": "HIGH",
  "confidence": 0.85,
  "response_type": "ai_generated",
  "matched_keywords": ["severe headache"],
  "timestamp": "2024-02-07T10:30:00"
}
```

### GET `/api/health`
Health check endpoint

## Severity Levels

| Level | Trigger | Action |
|-------|---------|--------|
| **CRITICAL** | Severe, life-threatening symptoms | Auto-dispatch ambulance |
| **HIGH** | Serious symptoms requiring medical attention | Auto-connect to doctor |
| **MODERATE** | Symptoms that should be monitored | Suggest doctor consultation |
| **LOW** | Mild symptoms | Provide guidance |

## Adding Custom Training Data

### To add more training data from GitHub:

1. Create a GitHub repository with health-related content
2. Update the `GITHUB_HEALTH_DATA` dictionary in `app.py`
3. Add your data in the relevant category:

```python
GITHUB_HEALTH_DATA = {
    'maternal': {
        'your_category': [
            'Your health information here',
            'Another health tip'
        ]
    }
}
```

## Fallback Mode

If OpenAI API is not available:
- Set `use_ai: false` in API request
- Chatbot will use template-based responses
- Still has knowledge base integration

## Cost Considerations

- **OpenAI API**: ~$0.0005 per 1000 tokens
- Typical chatbot response: 100-500 tokens (~$0.00005-$0.00025)
- Set up [usage limits](https://platform.openai.com/account/billing/limits) in OpenAI dashboard

## Troubleshooting

### Issue: "OpenAI API key not found"
- Ensure `.env` file exists in the project root
- Check that `OPENAI_API_KEY` is properly set
- Restart the Flask server

### Issue: "No module named 'openai'"
```bash
pip install openai==1.3.0 python-dotenv==1.0.0
```

### Issue: Slow responses
- OpenAI API calls may take 1-3 seconds
- Consider caching common responses
- Fallback to template mode for faster responses

## Frontend Integration

The chatbot automatically sends the `use_ai: true` flag. To toggle AI responses in the frontend:

```javascript
// In chatbot.js
const response = await fetch(this.apiUrl + '/api/chat', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    message: userMessage,
    patient_type: this.patientType,
    history: this.conversationHistory,
    use_ai: true  // Set to false for template-based responses
  })
});
```

## Next Steps

1. ✅ Deploy to production with proper API key management
2. ✅ Add more health data from public health GitHub repositories
3. ✅ Implement response caching for common questions
4. ✅ Add multilingual support
5. ✅ Fine-tune the model with your specific use cases

## Support

For issues with:
- **OpenAI API**: Visit [OpenAI Support](https://help.openai.com)
- **Flask/Backend**: Check the console logs
- **Chatbot UI**: Check browser console for errors

---

**Last Updated**: February 2024
**Version**: 2.0 (with Generative AI)
