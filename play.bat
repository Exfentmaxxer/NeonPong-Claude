@echo off
REM Quick launcher for Neon Pong (Windows)

REM Check if pygame is installed
python -c "import pygame" >nul 2>&1

if errorlevel 1 (
    echo Installing dependencies...
    python -m pip install pygame>=2.5.0 --quiet
)

REM Start the game
python pong_game.py
