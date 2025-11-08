#!/usr/bin/env python3
"""
Setup script for Neon Pong
"""

from setuptools import setup, find_packages
import sys
import subprocess

def install_and_run():
    """Install dependencies and optionally run the game"""
    print("=" * 60)
    print("  Installing Neon Pong")
    print("=" * 60)

    # Install dependencies
    print("\n[1/2] Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully!")
    except subprocess.CalledProcessError:
        print("✗ Failed to install dependencies")
        print("Please run manually: pip install pygame")
        sys.exit(1)

    print("\n[2/2] Setup complete!")
    print("=" * 60)
    print("  Neon Pong is ready to play!")
    print("=" * 60)
    print("\nTo start the game, run:")
    print("  python pong_game.py")
    print("\nOr use the launcher:")
    print("  python play.py")
    print()

    # Ask if user wants to start the game now
    try:
        response = input("Would you like to start the game now? (y/n): ").strip().lower()
        if response in ['y', 'yes']:
            print("\nStarting Neon Pong...")
            import pong_game
            pong_game.main()
    except KeyboardInterrupt:
        print("\n\nGame launch cancelled.")
    except Exception as e:
        print(f"\nCouldn't auto-start the game: {e}")
        print("You can start it manually with: python pong_game.py")

if __name__ == "__main__":
    install_and_run()
