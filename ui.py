import pygame
from settings import WHITE, BAR_BG_COLOR, BAR_FILL_COLOR, SCREEN_WIDTH, SAVINGS_MAX_SECONDS

class HUD:
    def __init__(self):
        # Use default font – replace later with bitmap font
        self.font = pygame.font.Font(None, 24)
        self.score = 0
        self.savings = SAVINGS_MAX_SECONDS  # seconds remaining

    # ---------------------------------------------------------
    # Public API
    # ---------------------------------------------------------
    def reset(self):
        self.score = 0
        self.savings = SAVINGS_MAX_SECONDS

    def add_score(self, points: int):
        self.score += points

    def add_savings(self, seconds: float):
        self.savings = min(self.savings + seconds, SAVINGS_MAX_SECONDS)

    def update(self, dt: float, running: bool = True):
        """dt = seconds since last frame."""
        if running and self.savings > 0:
            self.savings = max(self.savings - dt, 0)

    def draw(self, surface: pygame.Surface):
        # Savings bar (top‑left)
        bar_x, bar_y = 10, 10
        bar_w, bar_h = 150, 12
        ratio = self.savings / SAVINGS_MAX_SECONDS
        pygame.draw.rect(surface, BAR_BG_COLOR, (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(surface, BAR_FILL_COLOR, (bar_x, bar_y, bar_w * ratio, bar_h))
        pygame.draw.rect(surface, WHITE, (bar_x, bar_y, bar_w, bar_h), 1)

        # Score text below bar
        score_surf = self.font.render(f"Score: {self.score}", True, WHITE)
        surface.blit(score_surf, (bar_x, bar_y + bar_h + 6))