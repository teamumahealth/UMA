@echo off
REM UMA AI Chatbot - Quick Start Script
REM This script sets up and runs the UMA chatbot with generative AI

echo.
echo ====================================
echo UMA AI Chatbot - Quick Start Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org
    pause
    exit /b 1
)

echo Step 1: Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo Step 2: Setting up environment...

REM Check if .env exists
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo ⚠️  IMPORTANT: Edit the .env file and add your OpenAI API key!
    echo    1. Go to https://platform.openai.com/api-keys
    echo    2. Create a new API key
    echo    3. Paste it in the .env file: OPENAI_API_KEY=sk-...
    echo.
    echo Press any key to open the .env file...
    pause
    notepad .env
) else (
    echo .env file already exists
)

echo.
echo Step 3: Checking configuration...
python -c "import os; from dotenv import load_dotenv; load_dotenv(); key=os.getenv('OPENAI_API_KEY'); print('✅ OpenAI API Key configured') if key and key != 'your_openai_api_key_here' else print('⚠️  Warning: OpenAI API Key not properly set')"

echo.
echo ====================================
echo Starting UMA AI Chatbot Server...
echo ====================================
echo.
echo Server will run on: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause
