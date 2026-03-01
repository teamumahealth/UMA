# Testing the UMA Backend API

## Quick Start

1. **Start the Flask Backend Server:**
   ```bash
   python app.py
   ```
   
   You should see:
   ```
   * Running on http://127.0.0.1:5000
   * Debug mode: on
   ```

2. **Keep the server running** - Leave this terminal window open

3. **In a NEW terminal/command prompt, start the web server:**
   ```bash
   python -m http.server 8000
   ```

4. **Open your browser** and go to: `http://localhost:8000`

5. **Test the chatbot** - Click the chatbot button and try sending a message

## Verify API is Working

### Option 1: Browser Test
Open: `http://localhost:5000/api/health`

You should see: `{"status":"healthy","service":"UMA AI Chatbot API"}`

### Option 2: PowerShell Test
```powershell
Invoke-WebRequest -Uri "http://localhost:5000/api/health" -Method GET
```

### Option 3: Python Test
```python
import requests
response = requests.post('http://localhost:5000/api/chat', json={
    'message': 'I have severe bleeding',
    'patient_type': 'maternal',
    'history': []
})
print(response.json())
```

## Troubleshooting

**Server won't start?**
- Make sure port 5000 is not in use: `netstat -ano | findstr :5000`
- Check if Python dependencies are installed: `pip install -r requirements.txt`

**Getting CORS errors?**
- Make sure you're accessing the website through `http://localhost:8000` (not file://)
- The Flask server must be running when you access the website

**Chatbot shows connection error?**
- Verify Flask server is running (step 1)
- Check browser console (F12) for detailed error messages
- Make sure both servers are running simultaneously
