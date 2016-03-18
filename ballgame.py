import sys, pygame
import os

import entities

def main(argv):
    pygame.init()

    size    = (width, height) = 800, 600
    black   = 0, 0, 0
    clock   = pygame.time.Clock()

    screen      = pygame.display.set_mode(size)
    ball_img, _ = load_image("ball.gif")
    ball        = entities.Ball(ball_img, size)

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYUP and event.key == pygame.K_q:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                ball.bum(event.pos)

        ball.update(clock.tick())


        screen.fill(black)
        screen.blit(ball.image, ball.rect)
        pygame.display.flip()


def load_image(name):
    fp = os.path.join("resources", name)
    img = pygame.image.load(fp)
    return (img, img.get_rect())

main(sys.argv)
