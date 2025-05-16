"""Main loop and basic world rendering with forward‑looking camera & HUD."""

import sys
import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, BG_COLOR, CAMERA_LEAD_FRACTION
from player import Player
from ui import HUD

pygame.init()
pygame.display.set_caption("Job Hunt Runner – Prototype")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

# ---------------------------------------------------------
# Game objects
# ---------------------------------------------------------
all_sprites = pygame.sprite.Group()
player = Player((80, 350))
all_sprites.add(player)

hud = HUD()

# Camera
camera_x = 0

# Temporary ground rect for visual reference
GROUND_Y = 400

def run():
    global camera_x
    while True:
        dt_ms = clock.tick(FPS)
        dt = dt_ms / 1000.0

        # -------------------------------------
        # Event handling
        # -------------------------------------
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()

        # -------------------------------------
        # Update
        # -------------------------------------
        player.handle_input()
        all_sprites.update()

        # Lead camera: keep player 25 % from left edge
        target_cam_x = player.rect.left - SCREEN_WIDTH * CAMERA_LEAD_FRACTION
        camera_x += (target_cam_x - camera_x) * 0.1  # smooth lerp factor 0.1

        hud.update(dt)

        # -------------------------------------
        # Draw
        # -------------------------------------
        screen.fill(BG_COLOR)

        # Draw ground line for prototype
        pygame.draw.line(screen, (90, 90, 90), (0 - camera_x, GROUND_Y), (SCREEN_WIDTH - camera_x + 1600, GROUND_Y))

        # Draw sprites offset by camera
        for sprite in all_sprites:
            screen.blit(sprite.image, (sprite.rect.x - camera_x, sprite.rect.y))

        # HUD (not camera‑affected)
        hud.draw(screen)

        pygame.display.flip()

if __name__ == "__main__":
    run()
