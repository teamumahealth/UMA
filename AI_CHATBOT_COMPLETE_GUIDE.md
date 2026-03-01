# UMA AI Chatbot - Complete Documentation

## 🎯 What's New: Generative AI Integration

Your UMA health chatbot now features:

1. **🤖 OpenAI GPT-3.5-turbo Integration** - Intelligent, context-aware responses
2. **📚 GitHub Health Data** - Trained on medical knowledge from public repositories
3. **🔄 Conversation History** - Maintains context across multiple messages
4. **⚕️ Severity Detection** - Automatic escalation to doctors/ambulance
5. **🌍 Multi-language Ready** - Extensible for global health data

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture](#architecture)
3. [API Reference](#api-reference)
4. [Training Data](#training-data)
5. [Configuration](#configuration)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)

---

## Quick Start

### Prerequisites
- Python 3.8+
- OpenAI API key (free tier available)
- Modern web browser

### Installation

1. **Clone/Download the project**
   ```bash
   cd "UMA Website"
   ```

2. **Run the setup script** (Windows)
   ```bash
   setup_ai.bat
   ```
   
   Or **manual setup** (All platforms):
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   python app.py
   ```

3. **Access the chatbot**
   - Open your browser to `http://localhost:5000` (or where you host index.html)
   - The chatbot widget will appear in the bottom-right corner

4. **Start chatting!**
   ```
   User: "I have severe abdominal pain during pregnancy"
   UMA:  "🤖 AI-Powered Response
         I understand you're experiencing severe abdominal pain 
         during pregnancy. This requires immediate medical attention..."
   ```

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Browser)                    │
│  ┌──────────────────────────────────────────────────────┐   │
│  │         Chatbot UI (chatbot.js)                      │   │
│  │  - Message display                                   │   │
│  │  - User input handling                               │   │
│  │  - Conversation history                              │   │
│  └────────────────┬─────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                    │ HTTP POST/GET
                    ▼
┌─────────────────────────────────────────────────────────────┐
│                    Flask API Server (app.py)                │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Severity Detector                                   │   │
│  │  - Keyword matching (CRITICAL/HIGH/MODERATE/LOW)     │   │
│  │  - Conversation analysis                             │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  AI Response Generator                               │   │
│  │  - OpenAI GPT-3.5-turbo integration                  │   │
│  │  - Knowledge base context injection                  │   │
│  │  - Fallback template responses                       │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  GitHub Health Data (GITHUB_HEALTH_DATA)             │   │
│  │  - Maternal health information                       │   │
│  │  - Child health information                          │   │
│  │  - Medical guidelines                                │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                    │
        ┌───────────┼───────────┐
        ▼           ▼           ▼
    OpenAI API  GitHub API  Data Files
```

### Data Flow

```
User Message
    │
    ├─→ Severity Detection (app.py:detect_severity)
    │   - Extracts keywords
    │   - Calculates severity score
    │   - Determines urgency level
    │
    ├─→ AI Response Generation (app.py:generate_ai_response)
    │   - Retrieves relevant knowledge from GITHUB_HEALTH_DATA
    │   - Builds system prompt with medical context
    │   - Includes conversation history (last 3 messages)
    │   - Calls OpenAI API
    │   - Returns intelligent response
    │
    ├─→ Action Determination
    │   - CRITICAL → Auto-dispatch ambulance
    │   - HIGH → Auto-connect to doctor
    │   - MODERATE → Suggest consultation
    │   - LOW → Provide guidance
    │
    └─→ Response to User
        - Display with AI badge
        - Execute corresponding action
```

---

## API Reference

### POST `/api/chat`

**Generate a chatbot response**

#### Request
```json
{
  "message": "I have severe headache and dizziness",
  "patient_type": "maternal",
  "history": [
    {
      "type": "user",
      "message": "I'm 7 months pregnant"
    },
    {
      "type": "bot",
      "message": "Thank you for that information..."
    }
  ],
  "use_ai": true
}
```

#### Response
```json
{
  "message": "🤖 AI-Powered Response\nBased on your symptoms of severe headache and dizziness during pregnancy, this could indicate several conditions...",
  "action": "doctor",
  "severity": "HIGH",
  "confidence": 0.92,
  "matched_keywords": ["severe headache", "dizziness"],
  "response_type": "ai_generated",
  "timestamp": "2024-02-07T15:30:45.123Z"
}
```

#### Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `message` | string | ✓ | User's symptom description or question |
| `patient_type` | string | ✓ | Either `"maternal"` or `"child"` |
| `history` | array | | Previous messages in conversation |
| `use_ai` | boolean | | Default `true`. Set `false` for template responses |

#### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `message` | string | AI-generated or template response |
| `action` | string | Action to take: `"none"`, `"doctor"`, `"ambulance"` |
| `severity` | string | `"LOW"`, `"MODERATE"`, `"HIGH"`, or `"CRITICAL"` |
| `confidence` | number | 0.0 to 1.0 confidence score |
| `matched_keywords` | array | Keywords detected in message |
| `response_type` | string | `"ai_generated"` or `"template"` |
| `timestamp` | string | ISO 8601 timestamp |

#### Severity Levels

```
LOW (0.0 - 0.4)
├─ Mild symptoms
├─ General health questions
└─ Action: None (monitoring only)

MODERATE (0.4 - 0.6)
├─ Symptoms requiring monitoring
├─ Some symptoms present
└─ Action: Suggest doctor consultation

HIGH (0.6 - 0.85)
├─ Serious symptoms
├─ Multiple concerning symptoms
├─ Worsening conditions
└─ Action: Connect to doctor (AUTO)

CRITICAL (0.85 - 1.0)
├─ Life-threatening symptoms
├─ Emergency situation
├─ Immediate danger
└─ Action: Dispatch ambulance (AUTO)
```

### POST `/api/connect-doctor`

**Initiate doctor connection**

#### Request
```json
{
  "patient_info": {
    "type": "maternal",
    "history": [...]
  }
}
```

#### Response
```json
{
  "status": "success",
  "message": "Connecting you to Dr. Priya Sharma...",
  "doctor": {
    "name": "Dr. Priya Sharma",
    "specialization": "Obstetrics & Gynecology",
    "experience": "12 years",
    "status": "available"
  },
  "connection_time": "2024-02-07T15:32:00.000Z"
}
```

### POST `/api/call-ambulance`

**Dispatch emergency ambulance**

#### Request
```json
{
  "patient_info": {...},
  "location": "123 Main Street, City",
  "symptoms": "Severe chest pain, difficulty breathing"
}
```

#### Response
```json
{
  "status": "success",
  "message": "🚨 Ambulance dispatched! Arrival in 15-20 minutes",
  "ambulance": {
    "ambulance_id": "AMB-2024-001",
    "estimated_arrival": "15-20 minutes",
    "location": "123 Main Street, City",
    "priority": "CRITICAL"
  },
  "dispatch_time": "2024-02-07T15:33:00.000Z"
}
```

### GET `/api/health`

**Health check endpoint**

#### Response
```json
{
  "status": "healthy",
  "service": "UMA AI Chatbot API"
}
```

---

## Training Data

### Current Knowledge Base

#### Maternal Health
- **Pregnancy Complications**: Gestational diabetes, preeclampsia, placental issues
- **Nutrition**: Folic acid, iron, calcium, protein requirements
- **Prenatal Care**: Screening timeline, monitoring schedules

#### Child Health
- **Common Illnesses**: Cold, ear infections, throat issues, rashes
- **Immunization**: Complete vaccination schedule from birth
- **Safety**: Car seats, choking prevention, water safety, SIDS prevention

### Adding Custom Training Data

#### Method 1: Direct Python Update

Edit `app.py` and add to `GITHUB_HEALTH_DATA`:

```python
GITHUB_HEALTH_DATA = {
    'maternal': {
        'your_category': [
            'Health information point 1',
            'Health information point 2',
            'Health information point 3'
        ],
        # Add more...
    },
    'child': {
        # Similar structure
    }
}
```

#### Method 2: Fetch from GitHub

Use the provided scraper to fetch data from GitHub repositories:

```bash
python github_data_scraper.py
```

This will search for and display relevant health repositories:
- Maternal health resources
- Pediatric care guidelines
- Immunization schedules
- First aid information

### Data Sources

Quality health data can be sourced from:

1. **GitHub Repositories**
   - Health guidelines
   - Medical documentation
   - Clinical best practices

2. **Public Health Organizations**
   - CDC (Centers for Disease Control)
   - WHO (World Health Organization)
   - National health ministries

3. **Medical Literature**
   - PubMed research abstracts
   - Clinical trial data
   - Evidence-based guidelines

4. **Community Resources**
   - Patient education materials
   - Support group information
   - Local health programs

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# Required
OPENAI_API_KEY=sk-your-api-key-here

# Optional
GITHUB_TOKEN=ghp_your-github-token-here
DEBUG=true
FLASK_ENV=development
```

### OpenAI Configuration

The chatbot uses `gpt-3.5-turbo` by default. To change the model:

Edit `app.py` in the `generate_ai_response` method:

```python
response = self.client.chat.completions.create(
    model="gpt-4",  # Change to gpt-4 for better quality
    messages=messages,
    temperature=0.7,  # 0.0 = deterministic, 1.0 = creative
    max_tokens=500    # Maximum response length
)
```

### Temperature Settings

- **0.0-0.3**: Deterministic, factual responses (best for medical)
- **0.4-0.6**: Balanced responses (default: 0.7)
- **0.7-1.0**: Creative, varied responses

### Cost Optimization

1. **Use gpt-3.5-turbo** (cheapest, good for medical Q&A)
2. **Set max_tokens to 500** (limits response length)
3. **Cache common responses** (implement on frontend)
4. **Use fallback mode** for simple queries

---

## Examples

### Example 1: Maternal Health Query

```
User Input:
"I'm 8 months pregnant and having sharp abdominal pain"

Detected Severity: HIGH
Confidence: 0.89

System Prompt: [Context about maternal health, pregnancy complications]

User Message: "I'm 8 months pregnant and having sharp abdominal pain"

OpenAI Response:
"I understand you're experiencing sharp abdominal pain in your third 
trimester. While some discomfort is normal during pregnancy, sharp 
pain requires immediate evaluation. This could be:

1. Placental abruption - separation of placenta from uterus
2. Preeclampsia - high blood pressure condition
3. Labor - if you're near your due date
4. Ligament stretching - usually less concerning

⚠️ RECOMMENDED ACTION: Seek immediate medical attention. 
This is not something to wait out. Please go to the emergency room 
or call your healthcare provider immediately.

I'm connecting you to a healthcare professional right now."

Response Type: AI-Generated
Matched Keywords: ["sharp abdominal pain", "8 months pregnant"]
Action: doctor (auto-connect)
```

### Example 2: Child Health Query

```
User Input:
"My 6-month-old has high fever and won't eat"

Detected Severity: CRITICAL
Confidence: 0.92

System Prompt: [Context about infant health, critical symptoms]

OpenAI Response:
"High fever in a 6-month-old infant is a medical emergency. 
Infants this young cannot regulate their body temperature well, 
and fever can indicate serious conditions.

CRITICAL SYMPTOMS DETECTED:
• High fever (above 100.4°F is significant at this age)
• Refusing food (sign of illness or dehydration)

These require IMMEDIATE EVALUATION.

IMMEDIATE STEPS:
1. Do not delay - go to emergency room NOW
2. Bring all medical records
3. Note fever onset time and any other symptoms
4. Keep infant calm and relatively cool

⚠️ DO NOT rely on home care for this situation.

I am immediately dispatching an ambulance to your location. 
Please confirm your address and be ready."

Action: ambulance (auto-dispatch)
```

### Example 3: Mild Symptom Query

```
User Input:
"My child has a mild runny nose for 2 days"

Detected Severity: LOW
Confidence: 0.45

OpenAI Response:
"A mild runny nose for 2 days is typically a common cold, 
usually caused by a viral infection.

MANAGEMENT:
• Keep child hydrated with water, breast milk, or formula
• Use a humidifier to ease congestion
• Monitor for fever or other symptoms
• Most colds resolve in 5-7 days

WHEN TO SEEK MEDICAL CARE:
• High fever (over 101°F)
• Difficulty breathing
• Persistent cough lasting more than 2 weeks
• Drainage from ears
• Signs of dehydration

Continue monitoring at home. If symptoms worsen, 
contact your pediatrician."

Action: none (home care monitoring)
```

---

## Troubleshooting

### Issue 1: "API key not found" Error

**Symptoms**: Chatbot shows "OpenAI API key not found"

**Solution**:
1. Create `.env` file in project root
2. Add: `OPENAI_API_KEY=sk-your-key-here`
3. Restart Flask server: `python app.py`
4. Clear browser cache (Ctrl+Shift+Delete)

### Issue 2: "Connection timeout" Error

**Symptoms**: Slow responses or timeout errors

**Causes**: OpenAI API latency (1-3 seconds normal)

**Solutions**:
- Check internet connection: `ping api.openai.com`
- Check OpenAI status: https://status.openai.com
- Increase timeout in chatbot.js (default 30s)
- Use fallback mode: Set `use_ai: false` in request

### Issue 3: "No module named 'openai'"

**Symptoms**: ImportError when starting Flask

**Solution**:
```bash
pip install --upgrade openai python-dotenv
pip list | grep openai  # Verify installation
```

### Issue 4: Responses not using AI

**Symptoms**: Responses say "template" instead of "ai_generated"

**Causes**:
- OpenAI API key not set
- API rate limit exceeded
- Model not available in region

**Solution**:
```python
# Check in app.py
print(f"Client initialized: {client is not None}")
print(f"API Key set: {'OPENAI_API_KEY' in os.environ}")
```

### Issue 5: CORS Errors in Browser

**Symptoms**: "Access to XMLHttpRequest blocked by CORS policy"

**Solution**:
- Ensure Flask server is running
- Check CORS is enabled: `CORS(app)` in app.py
- Check API URL matches server: `http://localhost:5000`

---

## Advanced Usage

### Custom System Prompts

Create specialized prompts for different use cases:

```python
def get_custom_prompt(specialization='general'):
    prompts = {
        'obstetrics': 'You are a specialist in obstetrics...',
        'pediatrics': 'You are a pediatrician...',
        'emergency': 'You are an emergency medicine specialist...'
    }
    return prompts.get(specialization, prompts['general'])
```

### Multi-language Support

Extend to support multiple languages:

```python
GITHUB_HEALTH_DATA = {
    'en': {
        'maternal': {...},
        'child': {...}
    },
    'es': {
        'maternal': {...},
        'child': {...}
    }
}
```

### Analytics and Logging

Track interactions for improvement:

```python
@app.route('/api/chat', methods=['POST'])
def chat():
    # ... existing code ...
    
    # Log interaction
    log_interaction(message, severity, response_type)
    
    return jsonify(response)

def log_interaction(message, severity, response_type):
    with open('chatbot_logs.json', 'a') as f:
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'message': message,
            'severity': severity,
            'response_type': response_type
        }
        f.write(json.dumps(log_entry) + '\n')
```

---

## Performance Metrics

Typical response times:
- Severity detection: < 50ms
- OpenAI API call: 1-3 seconds
- Template fallback: < 100ms
- Total: 1-3.5 seconds average

To improve performance:
1. Enable response caching
2. Use gpt-3.5-turbo (faster than gpt-4)
3. Reduce max_tokens
4. Implement client-side validation

---

## Support & Resources

- **OpenAI Documentation**: https://platform.openai.com/docs
- **Flask Documentation**: https://flask.palletsprojects.com
- **GitHub API**: https://docs.github.com/en/rest
- **Health Data Sources**: CDC, WHO, NIH

---

## Version History

- **v2.0** (Feb 2024): Added generative AI, GitHub data integration
- **v1.0** (Jan 2024): Initial keyword-based chatbot

---

**Last Updated**: February 7, 2024
**Maintained By**: UMA Development Team
