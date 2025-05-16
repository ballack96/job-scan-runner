import pygame, random
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

TILE_SIZE = 16
CHUNK_W_TILES = 25
CHUNK_H_TILES = 15
CHUNK_PX_W = CHUNK_W_TILES * TILE_SIZE
CHUNK_PX_H = CHUNK_H_TILES * TILE_SIZE

class Chunk(pygame.sprite.Sprite):
    """Very simple ground‑only chunk: a platform spanning some width with optional gaps."""

    def __init__(self, gap_start=None, gap_width=0):
        super().__init__()
        self.image = pygame.Surface((CHUNK_PX_W, TILE_SIZE), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.gap_start = gap_start
        self.gap_width = gap_width
        self._render()

    def _render(self):
        self.image.fill((0, 0, 0, 0))
        if self.gap_start is None:
            pygame.draw.rect(self.image, (160, 80, 40), self.image.get_rect())
        else:
            # left part
            if self.gap_start > 0:
                pygame.draw.rect(self.image, (160, 80, 40), (0, 0, self.gap_start, TILE_SIZE))
            # right part
            right_x = self.gap_start + self.gap_width
            if right_x < CHUNK_PX_W:
                pygame.draw.rect(self.image, (160, 80, 40), (right_x, 0, CHUNK_PX_W - right_x, TILE_SIZE))

class ChunkManager:
    def __init__(self):
        self.chunks = pygame.sprite.Group()
        self.offset_x = 0  # how far world has scrolled
        # spawn two starter chunks
        first = Chunk()
        first.rect.topleft = (0, SCREEN_HEIGHT - TILE_SIZE)
        self.chunks.add(first)
        second = self._spawn_next(first)
        self.chunks.add(second)

    def _spawn_next(self, prev_chunk):
        kind = random.choice(["flat", "gap" if prev_chunk.gap_start is None else "flat"])
        if kind == "flat":
            new_chunk = Chunk()
        else:
            gap_start = random.randint(80, 200)
            gap_width = random.randint(48, 96)
            new_chunk = Chunk(gap_start, gap_width)
        new_chunk.rect.topleft = (prev_chunk.rect.right, prev_chunk.rect.top)
        return new_chunk

    def update(self, dx):
        self.offset_x += dx
        # remove off‑screen chunks & spawn new as needed
        left_boundary = -CHUNK_PX_W
        right_boundary = SCREEN_WIDTH + CHUNK_PX_W
        last_chunk = None
        for chunk in list(self.chunks):
            chunk.rect.x -= dx
            if chunk.rect.right < left_boundary:
                self.chunks.remove(chunk)
            last_chunk = chunk
        if last_chunk and last_chunk.rect.right < right_boundary:
            nxt = self._spawn_next(last_chunk)
            self.chunks.add(nxt)

    def draw(self, surface):
        self.chunks.draw(surface)

    def collide_rects(self):
        return [c.rect for c in self.chunks]