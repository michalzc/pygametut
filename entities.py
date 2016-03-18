import pygame
import random

MIN_START_SPEED = 100
MAX_START_SPEED = 200
WHITE = 255, 255, 255

FADE_RANGE = 500

class GameInfo(pygame.sprite.Sprite):
    def __init__(self, ball):
        pygame.sprite.Sprite.__init__(self)
        self.font = pygame.font.SysFont("Verdana", 12, False)
        self.fps = None
        self.ball = ball

        self.render_status()
        self.last_tick = 0

    def render_status(self):
        infos = [
            self.render_fps(),
            self.render_speed(),
            self.render_last_force()
        ]

        line_height = self.font.get_linesize()
        width = max([e.get_rect().width for e in infos])
        height = line_height * len(infos)
        image = pygame.surface.Surface((width, height)).convert()
        idx = 0
        for info in infos:
            rect = info.get_rect()
            rect.top = idx
            image.blit(info, rect)
            idx += line_height
        self.image = image
        self.rect = image.get_rect()


    def render_speed(self):
        txt = "Speed: (%.0f, %.0f)" % tuple(self.ball.speed)
        return self.font.render(txt, True, WHITE)

    def render_fps(self):
        fps = self.fps and ("%.0f" % self.fps) or "-"
        txt = "Fps: %s" % fps
        return self.font.render(txt, True, WHITE)

    def render_last_force(self):
        force = self.ball.last_force and ("%.0f, %.0f" % tuple(self.ball.last_force)) or "-, -"
        txt = "Last force: %s" % force
        return self.font.render(txt, True, WHITE)


    def update(self, tick, fps):
        self.last_tick += tick
        if self.last_tick > 300:
            self.last_tick = 0
            self.render_status()
            self.fps = fps



class Ball(pygame.sprite.Sprite):

    def __init__(self, image, board_size, start_position = None):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = image.get_rect()
        self.board_width, self.board_height = board_size
        self._init_position(start_position)
        self._init_speed()
        self.last_force = None

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

    def update(self, tick, *args):
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
            self.last_force = bum_vec
