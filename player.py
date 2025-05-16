"""Player sprite with tight platformer feel: jump, double‑jump, dash."""

import pygame
from settings import (GRAVITY, MAX_FALL_SPEED, RUN_ACCEL, RUN_DECEL, TOP_SPEED,
                      JUMP_IMPULSE, DOUBLE_JUMP_IMPULSE, DASH_SPEED, DASH_TIME,
                      COYOTE_FRAMES, JUMP_BUFFER_FRAMES, PLAYER_COLOR, K_LEFT, K_RIGHT, K_JUMP, K_DASH)

class Player(pygame.sprite.Sprite):
    WIDTH, HEIGHT = 24, 32

    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((self.WIDTH, self.HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect(topleft=pos)

        # Physics state
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.coyote_timer = 0
        self.jump_buffer = 0

        # Abilities
        self.can_double_jump = True
        self.dash_timer = 0
        self.dash_dir = pygame.Vector2(0, 0)

    # ---------------------------------------------------------
    # Input handling helpers
    # ---------------------------------------------------------
    def _key_pressed(self, keys, bindings):
        return any(keys[b] for b in bindings)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        # Horizontal movement
        move_dir = self._key_pressed(keys, K_RIGHT) - self._key_pressed(keys, K_LEFT)
        if move_dir != 0:
            self.vel.x += move_dir * RUN_ACCEL
        else:
            # Apply deceleration when no input
            if abs(self.vel.x) < RUN_DECEL:
                self.vel.x = 0
            else:
                self.vel.x -= RUN_DECEL * (1 if self.vel.x > 0 else -1)

        self.vel.x = max(-TOP_SPEED, min(TOP_SPEED, self.vel.x))

        # Jump
        if self._key_pressed(keys, K_JUMP):
            self.jump_buffer = JUMP_BUFFER_FRAMES
        else:
            self.jump_buffer = max(0, self.jump_buffer - 1)

        # Dash
        if self._key_pressed(keys, K_DASH) and self.dash_timer == 0:
            self.start_dash(keys)

    # ---------------------------------------------------------
    # Action routines
    # ---------------------------------------------------------
    def start_dash(self, keys):
        # Determine dash direction (8‑way)
        dir_x = self._key_pressed(keys, K_RIGHT) - self._key_pressed(keys, K_LEFT)
        dir_y = (keys[pygame.K_DOWN] - keys[pygame.K_UP]) if pygame.K_UP in keys else 0
        direction = pygame.Vector2(dir_x, dir_y)
        if direction.length_squared() == 0:
            direction.x = 1 if self.rect.width / 2 < 0 else -1  # default forward
        self.dash_dir = direction.normalize()
        self.dash_timer = DASH_TIME
        # Cancel vertical vel for crisp dash
        self.vel.y = 0

    def jump(self):
        self.vel.y = JUMP_IMPULSE
        self.on_ground = False
        self.can_double_jump = True

    def double_jump(self):
        self.vel.y = DOUBLE_JUMP_IMPULSE
        self.can_double_jump = False

    # ---------------------------------------------------------
    # Update loop
    # ---------------------------------------------------------
    def update(self):
        # Dash overrides normal movement
        if self.dash_timer > 0:
            self.rect.x += self.dash_dir.x * DASH_SPEED
            self.rect.y += self.dash_dir.y * DASH_SPEED
            self.dash_timer -= 1
            return

        # Apply gravity
        self.vel.y = min(self.vel.y + GRAVITY, MAX_FALL_SPEED)

        # Horizontal / vertical position update
        self.rect.x += round(self.vel.x)
        self.rect.y += round(self.vel.y)

        # Ground collision (simple flat ground for prototype)
        ground_y = 400  # temporary ground level
        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel.y = 0
            if not self.on_ground:
                self.on_ground = True
                self.can_double_jump = True
            self.coyote_timer = COYOTE_FRAMES
        else:
            self.on_ground = False
            self.coyote_timer = max(0, self.coyote_timer - 1)

        # Handle buffered jump / coyote time
        if self.jump_buffer and (self.on_ground or self.coyote_timer):
            self.jump()
            self.jump_buffer = 0

        # Double jump check
        keys = pygame.key.get_pressed()
        if self._key_pressed(keys, K_JUMP) and not self.on_ground and self.can_double_jump and self.jump_buffer:
            self.double_jump()
            self.jump_buffer = 0