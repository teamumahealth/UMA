# UMA MERN Stack - Quick Start Guide

## 🚀 Quick Setup (5 minutes)

### Step 1: Install Dependencies

**Windows:**
```bash
setup.bat
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Or manually:**
```bash
# Backend
cd backend
npm install

# Frontend
cd ../frontend
npm install
```

### Step 2: Setup MongoDB

**Option A: Local MongoDB**
1. Install MongoDB from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Start MongoDB service
3. Connection string: `mongodb://localhost:27017/uma-health`

**Option B: MongoDB Atlas (Cloud - Recommended)**
1. Sign up at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas) (Free tier available)
2. Create a cluster
3. Get your connection string (e.g., `mongodb+srv://username:password@cluster.mongodb.net/uma-health`)

### Step 3: Configure Environment

**Backend:**
```bash
cd backend
# Copy .env.example to .env
# Windows: copy .env.example .env
# macOS/Linux: cp .env.example .env
```

Edit `backend/.env`:
```
MONGODB_URI=mongodb://localhost:27017/uma-health
PORT=5000
NODE_ENV=development
```

**Frontend (Optional):**
Create `frontend/.env`:
```
REACT_APP_API_URL=http://localhost:5000/api
```

### Step 4: Start the Application

**Terminal 1 - Backend:**
```bash
cd backend
npm start
```
Backend runs on `http://localhost:5000`

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```
Frontend runs on `http://localhost:3000` (opens automatically)

### Step 5: Test the Application

1. Open `http://localhost:3000` in your browser
2. Click the chatbot button (bottom right)
3. Select patient type (Maternal or Child Health)
4. Try these test messages:
   - "I have a mild headache" (LOW severity)
   - "I have fever and vomiting" (HIGH severity - auto connects to doctor)
   - "I have severe bleeding" (CRITICAL - auto calls ambulance)

## 🎯 What to Expect

- **LOW Severity**: General advice, monitoring suggested
- **MODERATE Severity**: Doctor consultation recommended
- **HIGH Severity**: Automatically connects to doctor after 1.5 seconds
- **CRITICAL Severity**: Automatically dispatches ambulance after 2 seconds

## 🐛 Troubleshooting

### Backend won't start
- Check if MongoDB is running
- Verify `.env` file exists and has correct `MONGODB_URI`
- Check if port 5000 is available

### Frontend won't connect to backend
- Ensure backend is running on port 5000
- Check `REACT_APP_API_URL` in `frontend/.env`
- Check browser console for CORS errors

### MongoDB connection errors
- Verify MongoDB is running (local) or cluster is active (Atlas)
- Check connection string in `.env`
- For Atlas: Ensure IP whitelist includes your IP (0.0.0.0/0 for development)

## 📚 Next Steps

- Read `README_MERN.md` for detailed documentation
- Check API endpoints in `README_MERN.md`
- Customize severity detection in `backend/services/severityDetector.js`
- Modify UI components in `frontend/src/components/`

## 🆘 Need Help?

- Email: teamuma.health@gmail.com
- Instagram: @team_u.m.a
