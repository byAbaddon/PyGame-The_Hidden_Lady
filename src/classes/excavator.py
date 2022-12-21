import pygame

from src.settings import *
from src.classes.sound import Sound

class Excavator(pygame.sprite.Sprite, Sound):
    SPRITE_ANIMATION_SPEED = 0.3
    FRICTION = -0.12
    level = 1
    points = 0
    lives = 3
    # reset current data
    excavator_speed = 5
    current_ball_speed = 2
    counter_broken_bricks = 0
    game_timer = 0
    start_time = pygame.time.get_ticks()
    is_start_game_timer = False
    is_lost_ball = False
    is_level_complete = False
    is_game_over = False
    is_pause = False
    minutes = 0
    seconds = 0

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(f'./src/assets/images/excavator/sprite/1.png')
        self.sprites_move = [pygame.image.load(f'./src/assets/images/excavator/sprite/{x}.png') for x in range(1, 4)]
        self.current_sprite = 0
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.midbottom = (S_W // 4 + 30, S_H - FRAME_BLOCK_SIZE - 4)
        self.direction = vec(0, 0)
        self.pos = vec(self.rect.x, self.rect.y)
        self.acceleration = vec(1, 0)
        self.velocity = vec(0, 0)


    def move(self):
        if key_pressed(pygame.K_p):
            self.is_pause = True

        if key_pressed(pygame.K_RIGHT) and self.rect.x < START_FRAME_SIZE - self.image.get_width() - 10:
            self.direction.x = 1
            self.rect.x += self.excavator_speed
            Sound.engin(self)
        if key_pressed(pygame.K_LEFT) and self.rect.x > FRAME_BLOCK_SIZE + 10:
            self.direction.x = -1
            self.rect.x -= self.excavator_speed
            Sound.engin(self)

        self.acceleration.x += self.velocity.x * self.FRICTION
        self.velocity += self.acceleration * self.excavator_speed

    def sprite_frames(self):
        # left and right animation
        if check_key_pressed(pygame.K_LEFT) or check_key_pressed(pygame.K_RIGHT):
            self.current_sprite += self.SPRITE_ANIMATION_SPEED
            if self.current_sprite >= len(self.sprites_move):
                self.current_sprite = 1
            if self.direction.x == -1:
                self.image = self.sprites_move[int(self.current_sprite)]
            else:
                self.image = pygame.transform.flip(self.sprites_move[int(self.current_sprite)], True, False)

    def timer(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.start_time > 1000:
            self.start_time = time_now
            self.seconds += 1
            if self.seconds > 59:
                self.seconds = 0
                self.minutes += 1

    def reset_current_data(self):
        # self.counter_broken_bricks = 0
        self.game_timer = 0
        self.start_time = pygame.time.get_ticks()
        self.is_start_game_timer = False
        self.is_lost_ball = False
        self.is_pause = False
        self.minutes = 0
        self.seconds = 0
        self.rect.midbottom = (S_W // 4 + 30, S_H - FRAME_BLOCK_SIZE - 4)
        self.direction = vec(0, 0)
        self.pos = vec(self.rect.x, self.rect.y)
        self.acceleration = vec(1, 0)
        self.velocity = vec(0, 0)

    def reset_all_data(self):
        self.SPRITE_ANIMATION_SPEED = 0.3
        self.FRICTION = -0.12
        self.level = 1
        self.points = 0
        self.lives = 3
        self.excavator_speed = 5
        self.current_ball_speed = 2
        self.counter_broken_bricks = 0
        self.game_timer = 0
        self.start_time = pygame.time.get_ticks()
        self.is_start_game_timer = False
        self.is_lost_ball = False
        self.is_level_complete = False
        self.is_game_over = False
        self.is_pause = False
        self.minutes = 0
        self.seconds = 0
        self.current_sprite = 0
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.midbottom = (S_W // 4 + 30, S_H - FRAME_BLOCK_SIZE - 4)
        self.direction = vec(0, 0)
        self.pos = vec(self.rect.x, self.rect.y)
        self.acceleration = vec(1, 0)
        self.velocity = vec(0, 0)

    @staticmethod
    def draw_start_label():
        text_creator('Get Ready', 'teal', S_W // 4 + 10, S_H // 2, 30, None, './src/fonts/mario.ttf')
        text_creator('Press Space to Start', 'cornsilk', S_W // 7, S_H // 2 + 50, 26, None, './src/fonts/mario.ttf')

    def update(self):
        self.move()
        self.sprite_frames()
        if self.is_start_game_timer:
           self.timer()
        else:
            self.draw_start_label()



