@echo off
echo Starting Canadian Public Sector Training Lead Generation System...
echo ==================================================
echo.

echo Starting backend API on port 5000...
start /B python main.py
timeout /t 2 /nobreak > nul

echo Starting frontend on port 5001...
start /B python frontend.py

echo.
echo ==================================================
echo System is running!
echo.
echo Frontend: http://localhost:5001
echo API: http://localhost:5000/api/leads
echo.
echo Close this window to stop all services
echo ==================================================
echo.

pause