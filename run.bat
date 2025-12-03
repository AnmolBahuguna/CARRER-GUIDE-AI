@echo off
echo ========================================
echo   SmartCareer - Starting Application
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo Python found!
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Installing/Updating dependencies...
pip install -r requirements.txt --quiet

echo.
echo ========================================
echo   Starting Flask Application...
echo ========================================
echo.
echo Server will be available at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

pause





