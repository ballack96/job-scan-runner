import pygame
from settings import (
    GRAVITY, MAX_FALL_SPEED, RUN_ACCEL, RUN_DECEL, TOP_SPEED,
    JUMP_IMPULSE, DOUBLE_JUMP_IMPULSE, DASH_SPEED, DASH_TIME,
    COYOTE_FRAMES, JUMP_BUFFER_FRAMES
)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 32))
        self.image.fill((200, 200, 255))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.vel = pygame.Vector2(0, 0)
        self.on_ground = False
        self.coyote = 0
        self.jump_buffer = 0
        self.dash_timer = 0
        self.can_dash = True

    # ---------- INPUT HANDLING ----------
    def handle_input(self):
        keys = pygame.key.get_pressed()
        # Horizontal movement
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = min(self.vel.x + RUN_ACCEL, TOP_SPEED)
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = max(self.vel.x - RUN_ACCEL, -TOP_SPEED)
        else:
            # decel to zero
            if self.vel.x > 0:
                self.vel.x = max(0, self.vel.x - RUN_DECEL)
            elif self.vel.x < 0:
                self.vel.x = min(0, self.vel.x + RUN_DECEL)

        # Jump buffer
        if keys[pygame.K_SPACE] or keys[pygame.K_z]:
            self.jump_buffer = JUMP_BUFFER_FRAMES
        # Dash
        if (keys[pygame.K_x] or keys[pygame.K_LSHIFT]) and self.can_dash:
            self._start_dash(keys)

    # ---------- PHYSICS ----------
    def apply_gravity(self):
        if self.dash_timer <= 0:
            self.vel.y = min(self.vel.y + GRAVITY, MAX_FALL_SPEED)

    def _start_dash(self, keys):
        self.can_dash = False
        self.dash_timer = DASH_TIME
        dir_x = (keys[pygame.K_RIGHT] or keys[pygame.K_d]) - (keys[pygame.K_LEFT] or keys[pygame.K_a])
        dir_y = (keys[pygame.K_DOWN] or keys[pygame.K_s]) - (keys[pygame.K_UP] or keys[pygame.K_w])
        direction = pygame.Vector2(dir_x, dir_y)
        if direction.length_squared() == 0:
            direction.x = 1 if self.rect.centerx < 400 else -1  # default forward
        direction = direction.normalize()
        self.vel = direction * DASH_SPEED

    # ---------- UPDATE ----------
    def update(self, chunk_rects):
        self.handle_input()

        # Jump logic
        if self.jump_buffer > 0:
            if self.on_ground or self.coyote > 0:
                self.vel.y = -JUMP_IMPULSE
                self.on_ground = False
                self.coyote = 0
                self.jump_buffer = 0
            elif self.can_dash is False and self.dash_timer <= 0:
                # double jump when airborne and dash already used
                self.vel.y = -DOUBLE_JUMP_IMPULSE
                self.jump_buffer = 0
        if self.jump_buffer > 0:
            self.jump_buffer -= 1

        # Dash decay
        if self.dash_timer > 0:
            self.dash_timer -= 1
            if self.dash_timer == 0:
                self.vel *= 0.6  # slow after dash ends

        # Gravity
        self.apply_gravity()

        # Horizontal move & collide
        self.rect.x += int(self.vel.x)
        self._horizontal_collision(chunk_rects)
        # Vertical move & collide
        self.rect.y += int(self.vel.y)
        self._vertical_collision(chunk_rects)

        # Ground / coyote
        if self.on_ground:
            self.coyote = COYOTE_FRAMES
            self.can_dash = True
        else:
            if self.coyote > 0:
                self.coyote -= 1

    # ---------- COLLISION ----------
    def _horizontal_collision(self, solids):
        for s in solids:
            if self.rect.colliderect(s):
                if self.vel.x > 0:
                    self.rect.right = s.left
                elif self.vel.x < 0:
                    self.rect.left = s.right
                self.vel.x = 0

    def _vertical_collision(self, solids):
        self.on_ground = False
        for s in solids:
            if self.rect.colliderect(s):
                if self.vel.y > 0:
                    self.rect.bottom = s.top
                    self.vel.y = 0
                    self.on_ground = True
                elif self.vel.y < 0:
                    self.rect.top = s.bottom
                    self.vel.y = 0
