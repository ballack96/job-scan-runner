import pygame

"""Global settings and tweak‑able constants for the side‑scroller prototype."""

# Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
FPS = 60

# Physics – pixels / frame or frame² (60 FPS)
GRAVITY = 2                     # downward accel
MAX_FALL_SPEED = 16             # terminal velocity
RUN_ACCEL = 1.2                 # X accel when holding direction
RUN_DECEL = 0.8                 # X friction when no input
TOP_SPEED = 6                   # max run speed
JUMP_IMPULSE = -10              # initial jump velocity (negative = up)
DOUBLE_JUMP_IMPULSE = -9        # second jump a bit weaker

# Dash mechanics
DASH_SPEED = 12                 # pixels per frame burst
DASH_TIME = 9                   # frames the dash lasts (0.15 s @ 60 FPS)
COYOTE_FRAMES = 6               # grace after leaving an edge
JUMP_BUFFER_FRAMES = 6          # buffer input before landing

# Camera
CAMERA_LEAD_FRACTION = 0.25     # player stays 25 % from left edge

# HUD
SAVINGS_MAX_SECONDS = 30        # starting "health" timer in seconds

# Colors (RGB)
BG_COLOR = (25, 29, 38)
PLAYER_COLOR = (220, 90, 90)
BAR_BG_COLOR = (40, 40, 40)
BAR_FILL_COLOR = (0, 200, 0)
WHITE = (255, 255, 255)

# Key bindings (PyGame constants)
K_LEFT = (pygame.K_LEFT, pygame.K_a)
K_RIGHT = (pygame.K_RIGHT, pygame.K_d)
K_JUMP = (pygame.K_z, pygame.K_SPACE)
K_DASH = (pygame.K_x, pygame.K_LSHIFT)
