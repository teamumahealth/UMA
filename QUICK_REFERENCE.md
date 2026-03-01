# UMA AI Chatbot - Quick Reference

## 🚀 Getting Started (2 Minutes)

### Step 1: Install & Setup
```bash
pip install -r requirements.txt
copy .env.example .env
```

### Step 2: Add OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Create new key
3. Paste in `.env`:
   ```
   OPENAI_API_KEY=sk-your-key-here
   ```

### Step 3: Run Server
```bash
python app.py
```

Server runs on: `http://localhost:5000`

---

## 📊 Architecture at a Glance

```
User Asks Question
        ↓
Severity Detection (keyword matching)
        ↓
AI Response Generator (OpenAI GPT)
        ↓
+ Context (medical knowledge base)
+ Conversation history
+ Patient type info
        ↓
Smart Response
        ↓
Action (doctor/ambulance if needed)
```

---

## 🔑 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Flask backend, AI logic, API endpoints |
| `chatbot.js` | Frontend UI and interaction |
| `requirements.txt` | Python dependencies |
| `.env` | API keys (create from `.env.example`) |
| `github_data_scraper.py` | Fetch health data from GitHub |
| `AI_SETUP_GUIDE.md` | Detailed setup instructions |
| `AI_CHATBOT_COMPLETE_GUIDE.md` | Full documentation |

---

## 💬 API Quick Reference

### Chat Endpoint
```bash
POST http://localhost:5000/api/chat

{
  "message": "I have severe headache",
  "patient_type": "maternal",
  "history": [],
  "use_ai": true
}
```

**Response**: AI-generated health response with severity level

### Doctor Connection
```bash
POST http://localhost:5000/api/connect-doctor
```

### Ambulance Dispatch
```bash
POST http://localhost:5000/api/call-ambulance
```

---

## 🎯 Severity Levels

| Level | Score | Action | Example |
|-------|-------|--------|---------|
| 🟢 LOW | <0.4 | Monitor | Mild cold |
| 🟡 MODERATE | 0.4-0.6 | Check with doctor | Persistent cough |
| 🟠 HIGH | 0.6-0.85 | AUTO→Doctor | Severe pain |
| 🔴 CRITICAL | >0.85 | AUTO→Ambulance | Unconscious |

---

## 📚 Knowledge Base Structure

```python
GITHUB_HEALTH_DATA = {
    'maternal': {
        'pregnancy_complications': [...],
        'nutrition': [...],
        'prenatal_care': [...]
    },
    'child': {
        'common_illnesses': [...],
        'immunization': [...],
        'child_safety': [...]
    }
}
```

**Add your data here!**

---

## 🔧 Configuration

### Model Settings (in app.py)
```python
# Default: gpt-3.5-turbo (fast + cheap)
# Option: gpt-4 (smarter + expensive)

response = client.chat.completions.create(
    model="gpt-3.5-turbo",  # ← Change here
    temperature=0.7,         # 0=factual, 1=creative
    max_tokens=500          # Response length
)
```

### Temperature Guide
- **0.0-0.3**: Medical info (factual) ✅
- **0.4-0.6**: Balanced ✅
- **0.7-1.0**: Creative ⚠️

---

## 🐛 Common Issues

| Issue | Fix |
|-------|-----|
| "API key not found" | Check `.env` file, restart server |
| Slow responses | OpenAI normal latency 1-3s |
| "No module openai" | `pip install openai` |
| CORS errors | Ensure Flask running, check URL |
| Template responses | API key not set or API down |

---

## 📈 Performance Tips

1. **Cache responses** - Store common answers
2. **Use gpt-3.5-turbo** - Faster than gpt-4
3. **Reduce max_tokens** - Shorter responses
4. **Fallback mode** - Template responses for speed
5. **Batch requests** - If handling multiple users

---

## 🔗 Training Data Sources

1. **GitHub Health Repositories**
   - Run: `python github_data_scraper.py`

2. **Public Health APIs**
   - CDC: https://developer.cdc.gov
   - WHO: https://www.who.int/data

3. **Medical Databases**
   - PubMed: https://pubmed.ncbi.nlm.nih.gov
   - NIH: https://www.nih.gov

---

## 📝 Usage Examples

### Maternal Health
```
User: "I'm pregnant and bleeding"
UMA: [Severity: CRITICAL] 
     "This requires immediate medical attention.
      I'm dispatching an ambulance..."
```

### Child Health
```
User: "My baby has high fever"
UMA: [Severity: CRITICAL]
     "High fever in infants is serious.
      Emergency room now.
      Ambulance dispatched..."
```

### General Health
```
User: "I have a mild cough"
UMA: [Severity: LOW]
     "Common cold is usually self-limiting.
      Monitor for 5-7 days.
      Call doctor if symptoms worsen..."
```

---

## 🚀 Deployment Checklist

- [ ] Set strong OpenAI API key
- [ ] Use gpt-3.5-turbo (or gpt-4 if budget allows)
- [ ] Set max_tokens to 500
- [ ] Enable HTTPS
- [ ] Set up API rate limiting
- [ ] Monitor usage and costs
- [ ] Add error logging
- [ ] Test with real users
- [ ] Have fallback responses ready
- [ ] Regular backup of knowledge base

---

## 💰 Cost Breakdown

**Typical costs with gpt-3.5-turbo:**
- Input: ~$0.0005 per 1,000 tokens
- Output: ~$0.0015 per 1,000 tokens
- Per response: ~$0.0005-$0.001 (½-1 cent)

**Monthly estimate:**
- 1,000 chats: ~$0.50-$1.00
- 10,000 chats: ~$5-$10
- 100,000 chats: ~$50-$100

Set usage limits: https://platform.openai.com/account/billing/limits

---

## 🎓 Learning Path

1. **Beginner**: Run setup script, ask test questions
2. **Intermediate**: Modify knowledge base, test API
3. **Advanced**: Add custom prompts, fine-tune model
4. **Expert**: Implement caching, multi-language, analytics

---

## 📱 Frontend Integration

**Already integrated in chatbot.js:**
- ✅ Sends `use_ai: true` by default
- ✅ Shows "🤖 AI-Powered Response" badge
- ✅ Maintains conversation history
- ✅ Displays severity levels

**No changes needed!** Just add OpenAI key.

---

## 🔐 Security Best Practices

```python
# ✅ DO
- Store API key in .env (never commit)
- Use environment variables
- Add rate limiting
- Log interactions securely

# ❌ DON'T
- Hardcode API keys
- Share .env file
- Expose raw responses
- Trust user input without validation
```

---

## 📞 Support

- **Setup Issues**: See `AI_SETUP_GUIDE.md`
- **Full Docs**: See `AI_CHATBOT_COMPLETE_GUIDE.md`
- **API Errors**: Check OpenAI status page
- **Code Help**: See inline comments in `app.py`

---

## ⚡ Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment
copy .env.example .env

# Run server
python app.py

# Fetch GitHub health data
python github_data_scraper.py

# Test API
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"I have fever","patient_type":"child"}'

# Health check
curl http://localhost:5000/api/health
```

---

**Version 2.0 - AI-Powered Edition**
Last Updated: February 2024
