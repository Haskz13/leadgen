#!/bin/bash

echo "Starting Canadian Public Sector Training Lead Generation System..."
echo "=================================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Start backend API
echo "Starting backend API on port 5000..."
python3 main.py &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

# Wait a moment for backend to initialize
sleep 2

# Start frontend
echo "Starting frontend on port 5001..."
python3 frontend.py &
FRONTEND_PID=$!
echo "Frontend started with PID: $FRONTEND_PID"

echo ""
echo "=================================================="
echo "System is running!"
echo ""
echo "Frontend: http://localhost:5001"
echo "API: http://localhost:5000/api/leads"
echo ""
echo "Press Ctrl+C to stop all services"
echo "=================================================="

# Wait for Ctrl+C
trap "echo 'Stopping services...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait