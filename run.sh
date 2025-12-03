#!/bin/bash

echo "========================================"
echo "  SmartCareer - Starting Application"
echo "========================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ and try again"
    exit 1
fi

echo "Python found!"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Virtual environment not found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

echo ""
echo "Installing/Updating dependencies..."
pip install -r requirements.txt --quiet

echo ""
echo "========================================"
echo "  Starting Flask Application..."
echo "========================================"
echo ""
echo "Server will be available at: http://127.0.0.1:5000"
echo "Press Ctrl+C to stop the server"
echo ""

python3 app.py










