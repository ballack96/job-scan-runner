"""Main loop and basic world rendering with forward‑looking camera & HUD."""

# ---------------- game.py ----------------
import pygame, sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, CAMERA_LEAD
from player import Player
from chunk import ChunkManager
from ui import HUD

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def run():
    player = Player(100, SCREEN_HEIGHT - 80)
    chunks = ChunkManager()
    hud = HUD()
    all_sprites = pygame.sprite.Group(player)

    camera_x = 0

    running = True
    while running:
        dt = clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        # Update
        player.update(chunks.collide_rects())
        lead_target = player.rect.centerx - SCREEN_WIDTH * CAMERA_LEAD
        dx = int(lead_target - camera_x)
        camera_x += dx
        chunks.update(dx)
        hud.update()

        # Draw
        screen.fill((30, 30, 50))
        chunks.draw(screen)
        for spr in all_sprites:
            screen.blit(spr.image, (spr.rect.x - camera_x, spr.rect.y))
        hud.draw(screen)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    run()
