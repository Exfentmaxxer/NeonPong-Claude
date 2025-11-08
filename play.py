#!/usr/bin/env python3
"""
Neon Pong Launcher
Automatically checks dependencies and starts the game
"""

import sys
import subprocess

def check_and_install_pygame():
    """Check if pygame is installed, install if not"""
    try:
        import pygame
        print("✓ Pygame is installed")
        return True
    except ImportError:
        print("Pygame not found. Installing...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame>=2.5.0"])
            print("✓ Pygame installed successfully!")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install Pygame")
            print("\nPlease install manually:")
            print("  pip install pygame")
            return False

def main():
    """Main launcher function"""
    print("=" * 60)
    print("  NEON PONG LAUNCHER")
    print("=" * 60)
    print()

    # Check and install dependencies
    if not check_and_install_pygame():
        sys.exit(1)

    # Start the game
    print("\nStarting Neon Pong...")
    print("=" * 60)
    print()

    try:
        import pong_game
        pong_game.main()
    except Exception as e:
        print(f"\n✗ Error starting game: {e}")
        print("\nTry running directly:")
        print("  python pong_game.py")
        sys.exit(1)

if __name__ == "__main__":
    main()
