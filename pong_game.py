#!/usr/bin/env python3
"""
Neon Pong - A cyberpunk-themed Pong game
Features: AI opponent, particle effects, neon aesthetic, multiple game modes
"""

import pygame
import random
import math
import sys
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Constants
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FPS = 60

# Colors (Neon Cyberpunk Palette)
BLACK = (0, 0, 0)
DARK_BG = (10, 10, 20)
NEON_BLUE = (0, 255, 255)
NEON_PINK = (255, 0, 255)
NEON_GREEN = (0, 255, 100)
NEON_PURPLE = (200, 0, 255)
NEON_YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Game Settings
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
PADDLE_SPEED = 8
BALL_SIZE = 15
BALL_INITIAL_SPEED = 7
BALL_MAX_SPEED = 15
BALL_ACCELERATION = 0.3
WINNING_SCORE = 11

# Particle Settings
TRAIL_PARTICLE_COUNT = 3
EXPLOSION_PARTICLE_COUNT = 20


class GameState(Enum):
    """Game state enumeration"""
    MENU = 0
    PLAYING = 1
    PAUSED = 2
    GAME_OVER = 3


class Difficulty(Enum):
    """AI Difficulty levels"""
    EASY = 0
    MEDIUM = 1
    HARD = 2


@dataclass
class GameMode:
    """Game mode configuration"""
    single_player: bool
    difficulty: Difficulty = Difficulty.MEDIUM


class Particle:
    """Individual particle for visual effects"""

    def __init__(self, x: float, y: float, color: Tuple[int, int, int],
                 velocity: Optional[Tuple[float, float]] = None, lifetime: int = 30):
        self.x = x
        self.y = y
        self.color = color
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(2, 5)

        if velocity is None:
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
        else:
            self.vx, self.vy = velocity

    def update(self) -> bool:
        """Update particle position and lifetime. Returns False if particle is dead."""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        self.vx *= 0.98  # Friction
        self.vy *= 0.98
        return self.lifetime > 0

    def draw(self, screen: pygame.Surface):
        """Draw particle with alpha based on lifetime"""
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color_with_alpha = (*self.color, alpha)
        size = max(1, int(self.size * (self.lifetime / self.max_lifetime)))

        # Create surface with per-pixel alpha
        particle_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surf, color_with_alpha, (size, size), size)
        screen.blit(particle_surf, (int(self.x) - size, int(self.y) - size))


class ParticleSystem:
    """Manages all particles in the game"""

    def __init__(self):
        self.particles: List[Particle] = []

    def add_trail_particle(self, x: float, y: float, color: Tuple[int, int, int]):
        """Add a trail particle"""
        self.particles.append(Particle(x, y, color, lifetime=20))

    def add_explosion(self, x: float, y: float, color: Tuple[int, int, int], count: int = EXPLOSION_PARTICLE_COUNT):
        """Create an explosion effect"""
        for _ in range(count):
            self.particles.append(Particle(x, y, color, lifetime=40))

    def update(self):
        """Update all particles and remove dead ones"""
        self.particles = [p for p in self.particles if p.update()]

    def draw(self, screen: pygame.Surface):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(screen)


class Ball:
    """Ball class with physics and collision detection"""

    def __init__(self, x: float, y: float):
        self.reset(x, y)
        self.combo_hits = 0  # Track consecutive hits

    def reset(self, x: float, y: float):
        """Reset ball to center with random direction"""
        self.x = x
        self.y = y
        self.size = BALL_SIZE

        # Random initial direction
        angle = random.choice([
            random.uniform(-math.pi/4, math.pi/4),  # Right
            random.uniform(3*math.pi/4, 5*math.pi/4)  # Left
        ])

        self.vx = math.cos(angle) * BALL_INITIAL_SPEED
        self.vy = math.sin(angle) * BALL_INITIAL_SPEED
        self.speed = BALL_INITIAL_SPEED
        self.combo_hits = 0

    def update(self):
        """Update ball position"""
        self.x += self.vx
        self.y += self.vy

        # Top and bottom wall collision
        if self.y - self.size <= 0 or self.y + self.size >= WINDOW_HEIGHT:
            self.vy = -self.vy
            self.y = max(self.size, min(WINDOW_HEIGHT - self.size, self.y))
            return 'wall'

        return None

    def paddle_collision(self, paddle, particle_system: ParticleSystem) -> bool:
        """Check and handle paddle collision with angle-based deflection"""
        # Check if ball is in paddle x range
        ball_left = self.x - self.size
        ball_right = self.x + self.size
        paddle_left = paddle.x
        paddle_right = paddle.x + paddle.width

        # Check if ball overlaps paddle
        if not (ball_right >= paddle_left and ball_left <= paddle_right):
            return False

        # Check y overlap
        ball_top = self.y - self.size
        ball_bottom = self.y + self.size
        paddle_top = paddle.y
        paddle_bottom = paddle.y + paddle.height

        if ball_bottom >= paddle_top and ball_top <= paddle_bottom:
            # Collision detected!
            self.combo_hits += 1

            # Calculate hit position (-1 to 1, where 0 is center)
            hit_pos = (self.y - (paddle.y + paddle.height / 2)) / (paddle.height / 2)
            hit_pos = max(-1, min(1, hit_pos))

            # Calculate new angle based on hit position
            max_angle = math.pi / 3  # 60 degrees max
            angle = hit_pos * max_angle

            # Increase speed slightly
            self.speed = min(BALL_MAX_SPEED, self.speed + BALL_ACCELERATION)

            # Set new velocity
            direction = 1 if self.vx < 0 else -1  # Reverse horizontal direction
            self.vx = direction * math.cos(angle) * self.speed
            self.vy = math.sin(angle) * self.speed

            # Move ball outside paddle to prevent multiple collisions
            if direction < 0:
                self.x = paddle.x - self.size - 1
            else:
                self.x = paddle.x + paddle.width + self.size + 1

            # Create explosion effect
            particle_system.add_explosion(self.x, self.y, paddle.color,
                                         count=15 + self.combo_hits * 5)

            return True

        return False

    def is_out_of_bounds(self) -> Optional[str]:
        """Check if ball is out of bounds. Returns 'left' or 'right' or None"""
        if self.x + self.size < 0:
            return 'left'
        elif self.x - self.size > WINDOW_WIDTH:
            return 'right'
        return None

    def draw(self, screen: pygame.Surface, particle_system: ParticleSystem):
        """Draw ball with glow effect and trail particles"""
        # Add trail particles
        for _ in range(TRAIL_PARTICLE_COUNT):
            offset_x = random.uniform(-self.size/2, self.size/2)
            offset_y = random.uniform(-self.size/2, self.size/2)
            particle_system.add_trail_particle(
                self.x + offset_x,
                self.y + offset_y,
                NEON_YELLOW
            )

        # Draw glow (outer circle)
        glow_surf = pygame.Surface((self.size * 4, self.size * 4), pygame.SRCALPHA)
        for i in range(3, 0, -1):
            alpha = 50 // i
            pygame.draw.circle(glow_surf, (*NEON_YELLOW, alpha),
                             (self.size * 2, self.size * 2), self.size * i)
        screen.blit(glow_surf, (int(self.x) - self.size * 2, int(self.y) - self.size * 2))

        # Draw ball
        pygame.draw.circle(screen, NEON_YELLOW, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.size - 2)


class Paddle:
    """Paddle class with smooth movement"""

    def __init__(self, x: float, y: float, color: Tuple[int, int, int], is_ai: bool = False):
        self.x = x
        self.y = y
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.color = color
        self.is_ai = is_ai
        self.target_y = y
        self.speed = PADDLE_SPEED

    def move(self, dy: float):
        """Move paddle with boundary checking"""
        self.y += dy
        self.y = max(0, min(WINDOW_HEIGHT - self.height, self.y))

    def ai_update(self, ball: Ball, difficulty: Difficulty):
        """AI paddle movement with difficulty-based behavior"""
        # Predict ball position
        prediction_accuracy = {
            Difficulty.EASY: 0.3,
            Difficulty.MEDIUM: 0.6,
            Difficulty.HARD: 0.95
        }

        reaction_speed = {
            Difficulty.EASY: 0.5,
            Difficulty.MEDIUM: 0.7,
            Difficulty.HARD: 0.95
        }

        accuracy = prediction_accuracy[difficulty]
        react_speed = reaction_speed[difficulty]

        # Only track ball if it's moving towards AI
        if ball.vx > 0:
            # Add some randomness based on difficulty
            error = (1 - accuracy) * random.uniform(-100, 100)
            target = ball.y + error
        else:
            # Return to center when ball is moving away
            target = WINDOW_HEIGHT / 2

        # Smooth movement towards target
        center_y = self.y + self.height / 2
        diff = target - center_y

        if abs(diff) > 5:  # Dead zone to prevent jittering
            move_amount = diff * react_speed * 0.15
            self.move(move_amount)

    def draw(self, screen: pygame.Surface):
        """Draw paddle with glow effect"""
        # Draw glow
        glow_surf = pygame.Surface((self.width + 20, self.height + 20), pygame.SRCALPHA)
        for i in range(3, 0, -1):
            alpha = 40 // i
            pygame.draw.rect(glow_surf, (*self.color, alpha),
                           (10 - i * 3, 10 - i * 3, self.width + i * 6, self.height + i * 6),
                           border_radius=5)
        screen.blit(glow_surf, (int(self.x) - 10, int(self.y) - 10))

        # Draw paddle
        pygame.draw.rect(screen, self.color,
                        (int(self.x), int(self.y), self.width, self.height),
                        border_radius=5)


class SoundManager:
    """Manages game sound effects"""

    def __init__(self):
        self.enabled = True
        self.sounds = {}
        self._create_sounds()

    def _create_sounds(self):
        """Create procedural sound effects"""
        try:
            # Paddle hit sound (higher pitch)
            self.sounds['paddle'] = self._generate_beep(440, 100)
            # Wall hit sound (lower pitch)
            self.sounds['wall'] = self._generate_beep(220, 100)
            # Score sound
            self.sounds['score'] = self._generate_beep(330, 200)
            # Win sound
            self.sounds['win'] = self._generate_beep(550, 300)
        except:
            self.enabled = False
            print("Sound initialization failed. Continuing without sound.")

    def _generate_beep(self, frequency: int, duration: int) -> Optional[pygame.mixer.Sound]:
        """Generate a simple beep sound"""
        if not self.enabled:
            return None

        try:
            sample_rate = 22050
            n_samples = int(round(duration * sample_rate / 1000))

            # Generate sine wave
            buf = []
            for i in range(n_samples):
                value = int(4096 * math.sin(2 * math.pi * frequency * i / sample_rate))
                # Apply envelope to avoid clicks
                envelope = min(1.0, i / (n_samples * 0.1), (n_samples - i) / (n_samples * 0.1))
                value = int(value * envelope)
                buf.append([value, value])

            sound = pygame.sndarray.make_sound(buf)
            sound.set_volume(0.3)
            return sound
        except:
            return None

    def play(self, sound_name: str):
        """Play a sound effect"""
        if self.enabled and sound_name in self.sounds and self.sounds[sound_name]:
            self.sounds[sound_name].play()


class NeonPongGame:
    """Main game class"""

    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Neon Pong")
        self.clock = pygame.time.Clock()
        self.running = True

        # Game state
        self.state = GameState.MENU
        self.game_mode = GameMode(single_player=True, difficulty=Difficulty.MEDIUM)

        # Game objects
        self.particle_system = ParticleSystem()
        self.sound_manager = SoundManager()

        # Fonts
        self.title_font = pygame.font.Font(None, 100)
        self.menu_font = pygame.font.Font(None, 50)
        self.score_font = pygame.font.Font(None, 80)
        self.small_font = pygame.font.Font(None, 30)

        # Initialize game objects (will be reset on game start)
        self.ball = None
        self.paddle_left = None
        self.paddle_right = None
        self.score_left = 0
        self.score_right = 0
        self.winner = None

        # Menu state
        self.menu_selection = 0
        self.difficulty_selection = 1  # Default to Medium

    def reset_game(self):
        """Reset game state for a new game"""
        center_x = WINDOW_WIDTH // 2
        center_y = WINDOW_HEIGHT // 2

        self.ball = Ball(center_x, center_y)
        self.paddle_left = Paddle(30, center_y - PADDLE_HEIGHT // 2, NEON_BLUE)

        # Right paddle is AI or human based on game mode
        self.paddle_right = Paddle(
            WINDOW_WIDTH - 30 - PADDLE_WIDTH,
            center_y - PADDLE_HEIGHT // 2,
            NEON_PINK,
            is_ai=self.game_mode.single_player
        )

        self.score_left = 0
        self.score_right = 0
        self.winner = None
        self.particle_system = ParticleSystem()

    def handle_menu_input(self, event):
        """Handle menu input"""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu_selection = (self.menu_selection - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.menu_selection = (self.menu_selection + 1) % 3
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.menu_selection == 0:  # Single Player
                    self.game_mode.single_player = True
                    self.reset_game()
                    self.state = GameState.PLAYING
                elif self.menu_selection == 1:  # Two Player
                    self.game_mode.single_player = False
                    self.reset_game()
                    self.state = GameState.PLAYING
                elif self.menu_selection == 2:  # Quit
                    self.running = False
            elif event.key == pygame.K_LEFT and self.menu_selection == 0:
                self.difficulty_selection = (self.difficulty_selection - 1) % 3
                self.game_mode.difficulty = Difficulty(self.difficulty_selection)
            elif event.key == pygame.K_RIGHT and self.menu_selection == 0:
                self.difficulty_selection = (self.difficulty_selection + 1) % 3
                self.game_mode.difficulty = Difficulty(self.difficulty_selection)

    def handle_game_input(self):
        """Handle game input during play"""
        keys = pygame.key.get_pressed()

        # Player 1 controls (W/S)
        if keys[pygame.K_w]:
            self.paddle_left.move(-self.paddle_left.speed)
        if keys[pygame.K_s]:
            self.paddle_left.move(self.paddle_left.speed)

        # Player 2 controls (Up/Down) - only if not AI
        if not self.game_mode.single_player:
            if keys[pygame.K_UP]:
                self.paddle_right.move(-self.paddle_right.speed)
            if keys[pygame.K_DOWN]:
                self.paddle_right.move(self.paddle_right.speed)

    def update_game(self):
        """Update game state"""
        # Update AI
        if self.game_mode.single_player and self.paddle_right.is_ai:
            self.paddle_right.ai_update(self.ball, self.game_mode.difficulty)

        # Update ball
        collision = self.ball.update()
        if collision == 'wall':
            self.sound_manager.play('wall')

        # Check paddle collisions
        if self.ball.paddle_collision(self.paddle_left, self.particle_system):
            self.sound_manager.play('paddle')
        if self.ball.paddle_collision(self.paddle_right, self.particle_system):
            self.sound_manager.play('paddle')

        # Check scoring
        out = self.ball.is_out_of_bounds()
        if out:
            if out == 'left':
                self.score_right += 1
                self.particle_system.add_explosion(50, WINDOW_HEIGHT // 2, NEON_PINK, 30)
            else:
                self.score_left += 1
                self.particle_system.add_explosion(WINDOW_WIDTH - 50, WINDOW_HEIGHT // 2, NEON_BLUE, 30)

            self.sound_manager.play('score')

            # Check win condition
            if self.score_left >= WINNING_SCORE:
                self.winner = 'left'
                self.state = GameState.GAME_OVER
                self.sound_manager.play('win')
            elif self.score_right >= WINNING_SCORE:
                self.winner = 'right'
                self.state = GameState.GAME_OVER
                self.sound_manager.play('win')
            else:
                # Reset ball
                self.ball.reset(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)

        # Update particles
        self.particle_system.update()

    def draw_edge_glow(self):
        """Draw glowing edges around the screen"""
        glow_width = 3
        for i in range(glow_width):
            alpha = 100 - i * 30
            # Top
            pygame.draw.line(self.screen, (*NEON_PURPLE, alpha),
                           (0, i), (WINDOW_WIDTH, i), 2)
            # Bottom
            pygame.draw.line(self.screen, (*NEON_PURPLE, alpha),
                           (0, WINDOW_HEIGHT - i), (WINDOW_WIDTH, WINDOW_HEIGHT - i), 2)
            # Left
            pygame.draw.line(self.screen, (*NEON_BLUE, alpha),
                           (i, 0), (i, WINDOW_HEIGHT), 2)
            # Right
            pygame.draw.line(self.screen, (*NEON_PINK, alpha),
                           (WINDOW_WIDTH - i, 0), (WINDOW_WIDTH - i, WINDOW_HEIGHT), 2)

    def draw_menu(self):
        """Draw main menu"""
        self.screen.fill(DARK_BG)

        # Draw title with glow
        title_text = "NEON PONG"
        for offset in range(5, 0, -1):
            alpha = 50 // offset
            title_surf = self.title_font.render(title_text, True, NEON_PINK)
            title_surf.set_alpha(alpha)
            title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 150 - offset * 2))
            self.screen.blit(title_surf, title_rect)

        title_surf = self.title_font.render(title_text, True, WHITE)
        title_rect = title_surf.get_rect(center=(WINDOW_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)

        # Menu options
        menu_items = [
            "Single Player",
            "Two Players",
            "Quit"
        ]

        for i, item in enumerate(menu_items):
            color = NEON_GREEN if i == self.menu_selection else WHITE
            text_surf = self.menu_font.render(item, True, color)
            text_rect = text_surf.get_rect(center=(WINDOW_WIDTH // 2, 350 + i * 80))

            # Draw glow for selected item
            if i == self.menu_selection:
                for offset in range(3, 0, -1):
                    glow_surf = self.menu_font.render(item, True, color)
                    glow_surf.set_alpha(30)
                    glow_rect = glow_surf.get_rect(center=(WINDOW_WIDTH // 2, 350 + i * 80))
                    self.screen.blit(glow_surf, glow_rect)

            self.screen.blit(text_surf, text_rect)

            # Show difficulty selector for single player
            if i == 0:
                diff_names = ["EASY", "MEDIUM", "HARD"]
                diff_colors = [NEON_GREEN, NEON_YELLOW, NEON_PINK]
                diff_text = f"< {diff_names[self.difficulty_selection]} >"
                diff_color = diff_colors[self.difficulty_selection]

                diff_surf = self.small_font.render(diff_text, True, diff_color)
                diff_rect = diff_surf.get_rect(center=(WINDOW_WIDTH // 2, 390))
                self.screen.blit(diff_surf, diff_rect)

        # Instructions
        instructions = [
            "Player 1: W/S keys",
            "Player 2: Arrow keys",
            "SPACE to start | ESC to pause"
        ]

        for i, inst in enumerate(instructions):
            inst_surf = self.small_font.render(inst, True, NEON_BLUE)
            inst_rect = inst_surf.get_rect(center=(WINDOW_WIDTH // 2, 650 + i * 35))
            self.screen.blit(inst_surf, inst_rect)

        self.draw_edge_glow()

    def draw_game(self):
        """Draw game screen"""
        self.screen.fill(DARK_BG)

        # Draw center line
        for y in range(0, WINDOW_HEIGHT, 30):
            pygame.draw.rect(self.screen, (50, 50, 70),
                           (WINDOW_WIDTH // 2 - 2, y, 4, 20))

        # Draw particles
        self.particle_system.draw(self.screen)

        # Draw paddles
        self.paddle_left.draw(self.screen)
        self.paddle_right.draw(self.screen)

        # Draw ball
        self.ball.draw(self.screen, self.particle_system)

        # Draw scores with glow
        score_text_left = str(self.score_left)
        score_text_right = str(self.score_right)

        # Left score
        for offset in range(4, 0, -1):
            glow_surf = self.score_font.render(score_text_left, True, NEON_BLUE)
            glow_surf.set_alpha(30)
            self.screen.blit(glow_surf, (WINDOW_WIDTH // 4 - offset, 40 - offset))

        score_surf_left = self.score_font.render(score_text_left, True, NEON_BLUE)
        self.screen.blit(score_surf_left, (WINDOW_WIDTH // 4, 40))

        # Right score
        for offset in range(4, 0, -1):
            glow_surf = self.score_font.render(score_text_right, True, NEON_PINK)
            glow_surf.set_alpha(30)
            self.screen.blit(glow_surf, (3 * WINDOW_WIDTH // 4 - offset, 40 - offset))

        score_surf_right = self.score_font.render(score_text_right, True, NEON_PINK)
        self.screen.blit(score_surf_right, (3 * WINDOW_WIDTH // 4, 40))

        # Draw combo indicator if active
        if self.ball.combo_hits > 3:
            combo_text = f"COMBO x{self.ball.combo_hits}!"
            combo_surf = self.small_font.render(combo_text, True, NEON_YELLOW)
            combo_rect = combo_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50))
            self.screen.blit(combo_surf, combo_rect)

        self.draw_edge_glow()

    def draw_pause(self):
        """Draw pause overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))

        # Pause text
        pause_text = "PAUSED"
        pause_surf = self.title_font.render(pause_text, True, NEON_GREEN)
        pause_rect = pause_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 50))
        self.screen.blit(pause_surf, pause_rect)

        # Instructions
        inst_text = "Press ESC to resume"
        inst_surf = self.small_font.render(inst_text, True, WHITE)
        inst_rect = inst_surf.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 50))
        self.screen.blit(inst_surf, inst_rect)

    def draw_game_over(self):
        """Draw game over screen"""
        self.screen.fill(DARK_BG)

        # Winner announcement
        if self.winner == 'left':
            winner_text = "PLAYER 1 WINS!"
            winner_color = NEON_BLUE
        else:
            if self.game_mode.single_player:
                winner_text = "AI WINS!"
            else:
                winner_text = "PLAYER 2 WINS!"
            winner_color = NEON_PINK

        # Draw winner text with glow
        for offset in range(6, 0, -1):
            glow_surf = self.title_font.render(winner_text, True, winner_color)
            glow_surf.set_alpha(40)
            glow_rect = glow_surf.get_rect(center=(WINDOW_WIDTH // 2, 200))
            self.screen.blit(glow_surf, glow_rect)

        winner_surf = self.title_font.render(winner_text, True, WHITE)
        winner_rect = winner_surf.get_rect(center=(WINDOW_WIDTH // 2, 200))
        self.screen.blit(winner_surf, winner_rect)

        # Final score
        score_text = f"{self.score_left} - {self.score_right}"
        score_surf = self.score_font.render(score_text, True, NEON_GREEN)
        score_rect = score_surf.get_rect(center=(WINDOW_WIDTH // 2, 350))
        self.screen.blit(score_surf, score_rect)

        # Create celebration particles
        if random.random() < 0.3:
            x = random.randint(100, WINDOW_WIDTH - 100)
            y = random.randint(100, WINDOW_HEIGHT - 100)
            color = random.choice([NEON_BLUE, NEON_PINK, NEON_GREEN, NEON_YELLOW])
            self.particle_system.add_explosion(x, y, color, 10)

        self.particle_system.update()
        self.particle_system.draw(self.screen)

        # Instructions
        inst_text = "Press SPACE to play again | ESC for menu"
        inst_surf = self.small_font.render(inst_text, True, WHITE)
        inst_rect = inst_surf.get_rect(center=(WINDOW_WIDTH // 2, 500))
        self.screen.blit(inst_surf, inst_rect)

        self.draw_edge_glow()

    def run(self):
        """Main game loop"""
        while self.running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.state == GameState.MENU:
                    self.handle_menu_input(event)

                elif self.state == GameState.PLAYING:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = GameState.PAUSED

                elif self.state == GameState.PAUSED:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            self.state = GameState.PLAYING
                        elif event.key == pygame.K_q:
                            self.state = GameState.MENU

                elif self.state == GameState.GAME_OVER:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.reset_game()
                            self.state = GameState.PLAYING
                        elif event.key == pygame.K_ESCAPE:
                            self.state = GameState.MENU

            # Update
            if self.state == GameState.PLAYING:
                self.handle_game_input()
                self.update_game()
            elif self.state == GameState.MENU:
                # Update menu particles
                if random.random() < 0.1:
                    x = random.randint(0, WINDOW_WIDTH)
                    y = random.randint(0, WINDOW_HEIGHT)
                    color = random.choice([NEON_BLUE, NEON_PINK, NEON_GREEN])
                    self.particle_system.add_trail_particle(x, y, color)
                self.particle_system.update()

            # Draw
            if self.state == GameState.MENU:
                self.draw_menu()
                self.particle_system.draw(self.screen)
            elif self.state == GameState.PLAYING:
                self.draw_game()
            elif self.state == GameState.PAUSED:
                self.draw_game()
                self.draw_pause()
            elif self.state == GameState.GAME_OVER:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Entry point"""
    game = NeonPongGame()
    game.run()


if __name__ == "__main__":
    main()
