@echo off
echo ========================================
echo Pizza Management System - Quick Start
echo ========================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Starting Flask development server...
echo.
echo Default Login:
echo   Email: john.manager@pizzashop.com
echo   Password: password123
echo.
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py
