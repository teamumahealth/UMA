# UMA Quick Start Guide

## Quick Setup (5 minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Start Backend Server
```bash
python app.py
```
You should see: `Running on http://127.0.0.1:5000`

### Step 3: Open Website
- Open `index.html` in your browser, OR
- Use a local server:
  ```bash
  python -m http.server 8000
  ```
  Then visit: `http://localhost:8000`

### Step 4: Test the Chatbot
1. Click the chatbot button (bottom right)
2. Select patient type (Maternal/Child)
3. Try examples:
   - **Low severity**: "I feel a bit tired"
   - **Moderate**: "I have mild headache and nausea"
   - **High**: "I have fever and severe pain"
   - **Critical**: "I have severe bleeding and cannot breathe"

## Testing Severity Levels

### Critical Symptoms (Auto Ambulance)
- "severe bleeding"
- "unconscious"
- "cannot breathe"
- "seizure"
- "severe chest pain"

### High Severity (Auto Doctor Connection)
- "fever and vomiting"
- "severe pain"
- "contractions"
- "dizziness and fatigue"

### Moderate Severity
- "mild headache"
- "nausea"
- "tiredness"

### Low Severity
- General wellness questions
- Non-urgent concerns

## Troubleshooting

**Backend not connecting?**
- Ensure Flask server is running on port 5000
- Check browser console for CORS errors
- Verify `app.py` is running without errors

**Chatbot not appearing?**
- Check browser console for JavaScript errors
- Ensure `chatbot.js` and `chatbot.css` are loaded
- Clear browser cache and refresh

**API errors?**
- Verify all dependencies are installed: `pip list`
- Check Flask server logs for error messages
- Ensure port 5000 is not in use by another application

## Next Steps

- Review `README.md` for full documentation
- Customize severity detection keywords in `app.py`
- Integrate with real medical professional APIs
- Add location services for ambulance dispatch
- Deploy to production server
