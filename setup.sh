#!/bin/bash
# Setup script for Neon Pong (Linux/Mac)

echo "============================================================"
echo "  NEON PONG - Setup Script"
echo "============================================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "✗ Python 3 is not installed"
    echo "Please install Python 3.7 or higher from python.org"
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is available
if ! command -v pip3 &> /dev/null && ! python3 -m pip --version &> /dev/null; then
    echo "✗ pip is not installed"
    echo "Please install pip: python3 -m ensurepip"
    exit 1
fi

echo "✓ pip is available"
echo ""

# Install dependencies
echo "[1/2] Installing dependencies..."
python3 -m pip install -r requirements.txt --quiet --upgrade

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully!"
else
    echo "✗ Failed to install dependencies"
    echo "Try manually: pip3 install pygame"
    exit 1
fi

echo ""
echo "[2/2] Setup complete!"
echo "============================================================"
echo "  Neon Pong is ready to play!"
echo "============================================================"
echo ""
echo "To start the game:"
echo "  ./play.sh"
echo "  or"
echo "  python3 pong_game.py"
echo ""

# Make play script executable
chmod +x play.sh 2>/dev/null

# Ask if user wants to play now
read -p "Would you like to start the game now? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Starting Neon Pong..."
    python3 pong_game.py
fi
