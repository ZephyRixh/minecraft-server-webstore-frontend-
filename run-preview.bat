@echo off
echo Starting local preview server...
echo.
echo Opening browser...
timeout /t 2 /nobreak

start http://localhost:8000

echo.
echo Server running on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.

python server.py 8000
