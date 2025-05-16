# ---------------- settings.py ----------------
"""Global settings and tweak‑able constants for the prototype."""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 480
FPS = 60

# Physics
GRAVITY = 2
MAX_FALL_SPEED = 16
RUN_ACCEL = 1.2
RUN_DECEL = 1.0
TOP_SPEED = 6
JUMP_IMPULSE = 10
DOUBLE_JUMP_IMPULSE = 9
DASH_SPEED = 12
DASH_TIME = 9          # frames (~0.15 s at 60 FPS)
COYOTE_FRAMES = 6
JUMP_BUFFER_FRAMES = 6

# Camera lead (fraction of screen width ahead of player)
CAMERA_LEAD = 0.25

# HUD
SAVINGS_MAX = 30        # seconds of savings (bar drains 1 px / s)