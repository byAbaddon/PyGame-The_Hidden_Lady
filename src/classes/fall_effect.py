import pygame
from src.settings import SCREEN, S_W, S_H, FRAME_SIZE, randrange


class FallEffect:
    effect_list = []
    start_time = pygame.time.get_ticks()
    COOLDOWN = 1000

    def __init__(self):
        self.speed = 50

    def fail_effect_creator(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.start_time > self.COOLDOWN:
            self.start_time = time_now
            x = randrange(0, S_W)
            y = randrange(0, S_H)
            self.effect_list.append([x, y])

    def confetti_creator(self):
        for i in self.effect_list:
            i[1] += self.speed  # add speed gravity
            if i[1] > S_H - FRAME_SIZE:
                i[0] = randrange(BLOCK_SIZE,  S_W - BLOCK_SIZE)
                i[1] = randrange(BLOCK_SIZE, S_H - FRAME_SIZE)
            pygame.draw.line(SCREEN, (randrange(0, 255), randrange(0, 255), randrange(0, 255)), i,
                             (i[0] - 1, i[1] + 15), randrange(1, 10))
        if len(self.effect_list) > 100:
            self.effect_list = self.effect_list[:100]
            # pygame.draw.circle(SCREEN, (randrange(0, 255), randrange(0, 255), randrange(0, 255)), i, randrange(5, 10))

    def update(self):
        self.fail_effect_creator()
        self.confetti_creator()
