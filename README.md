# Neon Pong

A cyberpunk-themed Pong game with stunning visual effects, particle systems, and multiple game modes.

![Game Preview](https://img.shields.io/badge/Python-3.7+-blue.svg) ![Pygame](https://img.shields.io/badge/Pygame-2.5.0+-green.svg)

## Features

### Core Gameplay
- **Classic Pong mechanics** with smooth 60 FPS gameplay
- **Realistic ball physics** with angle-based deflection on paddle hits
- **Dynamic difficulty** - ball speed increases with each paddle hit
- **Score tracking** with win condition (first to 11 points)
- **Combo system** - consecutive hits create more spectacular effects

### Visual Effects
- **Neon cyberpunk aesthetic** with glowing elements
- **Particle explosion effects** on ball/paddle collisions
- **Particle trails** following the ball movement
- **Screen edge glow effects** in neon colors
- **Animated score display** with glow effects
- **Color-coded elements** - Blue for Player 1, Pink for Player 2/AI
- **Celebration particles** on the game over screen

### Game Modes
- **Single Player** - Challenge AI opponents with 3 difficulty levels:
  - **Easy** - Slower reaction time, less accurate prediction
  - **Medium** - Balanced gameplay
  - **Hard** - Lightning-fast reactions, near-perfect prediction
- **Two Player Local Multiplayer** - Play against a friend on the same keyboard
- **Pause functionality** - Press ESC to pause/resume during gameplay
- **Polished menus** - Main menu and game over screen with replay options

### Controls
- **Player 1:**
  - `W` - Move paddle up
  - `S` - Move paddle down

- **Player 2 (Two Player Mode):**
  - `↑` (Up Arrow) - Move paddle up
  - `↓` (Down Arrow) - Move paddle down

- **General:**
  - `SPACE` - Start game / Play again
  - `ESC` - Pause game / Return to menu
  - `←/→` (Arrow keys) - Change AI difficulty in menu
  - `ENTER` - Select menu option

### Sound Effects
- Procedurally generated sound effects for:
  - Paddle hits (high pitch beep)
  - Wall bounces (lower pitch beep)
  - Scoring (medium pitch)
  - Victory (celebration sound)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. **Clone or download this repository**
   ```bash
   git clone <repository-url>
   cd NeonPong-Claude
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   Or install Pygame directly:
   ```bash
   pip install pygame
   ```

## Running the Game

Simply run the main game file:

```bash
python pong_game.py
```

Or make it executable (Linux/Mac):
```bash
chmod +x pong_game.py
./pong_game.py
```

## How to Play

1. **Launch the game** - Run `pong_game.py`
2. **Select game mode** - Use arrow keys to navigate the menu
3. **Choose difficulty** (Single Player only) - Use left/right arrows
4. **Start playing** - Press SPACE or ENTER
5. **Score points** - Make your opponent miss the ball
6. **Win the game** - First player to 11 points wins!

### Gameplay Tips
- **Aim your shots** - Hit the ball with the edge of your paddle to create sharper angles
- **Build combos** - Consecutive hits create more spectacular visual effects
- **Watch the speed** - The ball accelerates with each hit, up to a maximum speed
- **AI difficulty** - Start with Easy to learn, then challenge yourself with Hard mode

## Technical Details

### Architecture
The game is built with a clean, modular architecture:

- **`Ball` class** - Handles ball physics, collision detection, and rendering
- **`Paddle` class** - Manages paddle movement, AI behavior, and rendering
- **`Particle` class** - Individual particle for visual effects
- **`ParticleSystem` class** - Manages all particles in the game
- **`SoundManager` class** - Handles procedural sound generation and playback
- **`NeonPongGame` class** - Main game loop and state management

### Performance
- Locked to **60 FPS** for smooth, consistent gameplay
- Efficient particle system with automatic cleanup
- Optimized rendering with per-pixel alpha for glow effects
- Minimal CPU usage during menu and pause states

### Game States
- `MENU` - Main menu for mode selection
- `PLAYING` - Active gameplay
- `PAUSED` - Game paused
- `GAME_OVER` - Victory screen with replay option

## Customization

You can easily customize the game by modifying constants at the top of `pong_game.py`:

```python
# Window settings
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Paddle settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8

# Ball settings
BALL_SIZE = 15
BALL_INITIAL_SPEED = 7
BALL_MAX_SPEED = 15
BALL_ACCELERATION = 0.3

# Game settings
WINNING_SCORE = 11

# Colors (RGB tuples)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
NEON_GREEN = (0, 255, 100)
# ... and more
```

## Troubleshooting

### No sound
If sound doesn't work, the game will continue without audio. This is usually due to:
- Missing audio drivers
- Incompatible audio system
- The game automatically detects this and disables sound

### Performance issues
If the game runs slowly:
- Close other applications
- Reduce particle count by modifying `TRAIL_PARTICLE_COUNT` and `EXPLOSION_PARTICLE_COUNT`
- Ensure your Python installation is up to date

### Display issues
If graphics appear incorrect:
- Update your graphics drivers
- Ensure Pygame is properly installed: `pip install --upgrade pygame`

## License

This project is open source and available for educational and personal use.

## Credits

Built with:
- **Python** - Programming language
- **Pygame** - Game development library
- **Love** - And a passion for retro gaming with modern aesthetics

## Future Enhancements

Potential features for future versions:
- Online multiplayer
- Power-ups and special abilities
- Multiple ball modes
- Tournament mode with brackets
- Leaderboard system
- Custom color themes
- Configurable controls
- Replay system

---

**Enjoy the game!** 🎮✨

For issues, suggestions, or contributions, please open an issue or pull request.
