@echo off
echo ====================================
echo UMA MERN Stack Setup
echo ====================================
echo.

echo Installing backend dependencies...
cd backend
call npm install
if errorlevel 1 (
    echo Backend installation failed!
    pause
    exit /b 1
)
cd ..

echo.
echo Installing frontend dependencies...
cd frontend
call npm install
if errorlevel 1 (
    echo Frontend installation failed!
    pause
    exit /b 1
)
cd ..

echo.
echo ====================================
echo Setup Complete!
echo ====================================
echo.
echo Next steps:
echo 1. Make sure MongoDB is running
echo 2. Create backend/.env file with MONGODB_URI
echo 3. Start backend: cd backend ^&^& npm start
echo 4. Start frontend: cd frontend ^&^& npm start
echo.
pause
