import pygame
import random

MIN_START_SPEED = 100
MAX_START_SPEED = 200

FADE_RANGE = 500

class Ball(pygame.sprite.Sprite):

    def __init__(self, image, board_size, start_position = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.board_width, self.board_height = board_size
        self._init_position(start_position)
        self._init_speed()

    def board_size(self):
        return (self.board_width, self.board_height)

    def _init_position(self, start_position):
        if start_position:
            self.position = start_position
            self.rect.topleft = start_position
        else:
            x = random.randrange(0, self.board_width - self.rect.width)
            y = random.randrange(0, self.board_height - self.rect.height)
            self.position = (x,y)
            self.rect.topleft = (x,y)

    def _init_speed(self):
        x = random.randrange(MIN_START_SPEED, MAX_START_SPEED + 1)
        y = random.randrange(MIN_START_SPEED, MAX_START_SPEED + 1)
        x *= random.choice((-1,1))
        y *= random.choice((-1,1))

        self.speed = pygame.math.Vector2(x, y)

    def update(self, tick):
        f = tick / 1000
        x, y = self.position
        xs, ys = self.speed

        x = x + (xs * f)
        y = y + (ys * f)

        self.position = (x,y)
        self.rect.topleft = (x,y)

        if self.rect.left < 0:
            xs = abs(xs)
        elif self.rect.right > self.board_width:
            xs = -abs(xs)

        if self.rect.top < 0:
            ys = abs(ys)
        elif self.rect.bottom > self.board_height:
            ys = -abs(ys)

        self.speed = pygame.math.Vector2(xs, ys)

    def bum(self, pos):
        cx, cy = self.rect.center
        px, py = pos

        bum_vec = pygame.math.Vector2(cx - px, cy - py)
        bum_force = FADE_RANGE - bum_vec.length()
        if bum_force > 0:
            bum_vec = bum_vec.normalize() * bum_force
            self.speed += bum_vec
