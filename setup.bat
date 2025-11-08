@echo off
REM Setup script for Neon Pong (Windows)

echo ============================================================
echo   NEON PONG - Setup Script
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed
    echo Please install Python 3.7 or higher from python.org
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo + Python found
python --version
echo.

REM Install dependencies
echo [1/2] Installing dependencies...
python -m pip install -r requirements.txt --quiet --upgrade

if errorlevel 1 (
    echo X Failed to install dependencies
    echo Try manually: pip install pygame
    pause
    exit /b 1
)

echo + Dependencies installed successfully!
echo.

echo [2/2] Setup complete!
echo ============================================================
echo   Neon Pong is ready to play!
echo ============================================================
echo.
echo To start the game:
echo   play.bat
echo   or
echo   python pong_game.py
echo.

REM Ask if user wants to play now
set /p response="Would you like to start the game now? (y/n): "
if /i "%response%"=="y" (
    echo.
    echo Starting Neon Pong...
    python pong_game.py
)

pause
