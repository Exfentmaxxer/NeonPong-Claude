#!/bin/bash
# Quick launcher for Neon Pong (Linux/Mac)

# Check if pygame is installed
python3 -c "import pygame" 2>/dev/null

if [ $? -ne 0 ]; then
    echo "Installing dependencies..."
    python3 -m pip install pygame>=2.5.0 --quiet
fi

# Start the game
python3 pong_game.py
