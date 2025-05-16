import pygame, time
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SAVINGS_MAX

FONT = None

def _get_font():
    global FONT
    if FONT is None:
        FONT = pygame.font.SysFont("Consolas", 18)
    return FONT

class HUD:
    def __init__(self):
        self.savings = SAVINGS_MAX
        self.score = 0
        self.last_time = time.perf_counter()

    def add_savings(self, amount):
        self.savings = min(SAVINGS_MAX, self.savings + amount)

    def add_score(self, pts):
        self.score += pts

    def update(self):
        now = time.perf_counter()
        dt = now - self.last_time
        self.last_time = now
        self.savings = max(0, self.savings - dt)

    def draw(self, surface):
        # Savings bar
        bar_w = int((self.savings / SAVINGS_MAX) * 150)
        pygame.draw.rect(surface, (40, 160, 40), (10, 10, bar_w, 16))
        pygame.draw.rect(surface, (255, 255, 255), (10, 10, 150, 16), 2)
        # Score text
        txt = _get_font().render(f"Score: {self.score}", True, (255, 255, 255))
        surface.blit(txt, (10, 32))