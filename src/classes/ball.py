import pygame.time

from src.settings import *
from src.classes.sound import Sound
class Ball(pygame.sprite.Sprite, Sound):
    is_start_game = False
    is_start_game_timer = False

    def __init__(self, all_spite_groups_dict, excavator):
        pygame.sprite.Sprite.__init__(self)
        self.asg = all_spite_groups_dict
        self.excavator_data = excavator
        self.image = pygame.image.load(f'./src/assets/images/ball/1.png')
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = self.excavator_data.rect.midtop
        self.pos = vec(self.rect.midbottom)
        self.direction = vec(0, 0)
        self.speed = self.excavator_data.current_ball_speed

    def move(self):
        if not self.is_start_game: # ----------- before start
            self.rect.x = self.excavator_data.rect.x + self.excavator_data.image.get_width() // 2
            self.rect.y = self.excavator_data.rect.y - 22  # fix to 19
        # -------------------------------------- start
        if key_pressed(pygame.K_SPACE) and not self.is_start_game:
            self.direction = vec(choice([-1, 1]), -1)
            self.is_start_game = True
        # ---------------------------------------after start - infinity move ball
        if self.is_start_game:
            self.rect.x += self.direction.x * self.speed
            self.rect.y += self.direction.y * self.speed
            self.excavator_data.is_start_game_timer = True

    # check and fix BUG
    def check_ball_in_frame_bug(self):
        if self.rect.x < FRAME_BLOCK_SIZE or self.rect.x > START_FRAME_SIZE:  # bug
            if self.rect.x < FRAME_BLOCK_SIZE:
                self.rect.x += 10
            if self.rect.x > START_FRAME_SIZE:
                self.rect.x -= 10
        if self.rect.x < FRAME_BLOCK_SIZE or self.rect.x > START_FRAME_SIZE:
            self.rect.y = S_H // 2
            text_creator('Wow! You get BUG.', 'red', 50, S_H // 2, 26, None, './src/fonts/mario.ttf')
            text_creator('Bonus 3000 points', 'green', 50, S_H // 2 + 40, 22, None, './src/fonts/mario.ttf')
            text_creator('Press Return to resset ball position.', 'white', 50, S_H // 2 + 80, 22, None, './src/fonts/mario.ttf')
            if key_pressed(pygame.K_RETURN):
                self.rect.center = self.excavator_data.rect.midtop
                self.pos = vec(self.rect.midbottom)
                self.direction = vec(0, 0)
                self.excavator_data.points += 3000

    def check_collide_in_wall(self):
        if self.rect.x < FRAME_BLOCK_SIZE + 5 or self.rect.x > START_FRAME_SIZE - 20: # collide left / right
            if self.direction.x == -1:
                self.direction.x = 1
            else:
                self.direction.x = -1

        if self.rect.y < FRAME_BLOCK_SIZE: # collide top
            if self.direction.y == -1:
                self.direction.y = 1
            else:
                self.direction.y = -1

        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

        # -------------------  check if lost ball
        if self.rect.y > 492:
            self.excavator_data.lives -= 1
            if self.excavator_data.lives == 0:
                self.excavator_data.is_game_over = True
            else:
                self.excavator_data.is_lost_ball = True
                if self.excavator_data.lives > 0:
                    Sound.stop_all_sounds()
                Sound.lost_ball(self)
                text_creator(f'You lost ball', 'red', S_W // 4 + 10, S_H // 2, 30, None, './src/fonts/mario.ttf', True)

    def check_collide_in_tile(self):
        brick_buffer = 5
        bricks_group = self.asg['tile']
        for sprite in pygame.sprite.spritecollide(self, bricks_group, True, pygame.sprite.collide_mask):
            Sound.break_brick(self)
            self.excavator_data.counter_broken_bricks += 1
            # change ball direction
            # ================================ x
            # ----HIT-UP----
            # --------------------ball go down and hit top  brick /   if True  reverse x direction
            if self.direction.x == -1:
                if sprite.rect.top + brick_buffer>= self.rect.bottom: # hit tile top
                    self.direction.x = -1
                else:
                    self.direction.x = 1
            else:
                if sprite.rect.top + brick_buffer >= self.rect.bottom: # hit tile top
                    self.direction.x = 1
                else:
                    self.direction.x = -1
            # -----HIT-LEFT/RIGHT
            # -------------------- ball go right and hit left side brick /   if True  reverse x direction
            if sprite.rect.left + brick_buffer >= self.rect.right:
                self.direction.x = -1

            # -------AUTO------------- ball go left and hit right side brick /   if True  reverse x direction
            if sprite.rect.right  <= self.rect.left + brick_buffer:
                self.direction.x = 1

            # -----HIT BOTTOM
            # ----- ball go up and hit right side brick  / if True reverse x direction
            if sprite.rect.midbottom[0] >= self.rect.x:
                if self.direction.x == 1:
                    self.direction.x = -1
                else:
                    self.direction.x = 1

            # ====================================  y
            if self.direction.y == -1:
                self.direction.y = 1
            else:
                self.direction.y = -1

            # ----------------------------------- get power and ADD points of current brick number:
            self.excavator_data.points += 100 * sprite.random_brick_num

    def check_collide_in_excavator(self):
        excavator_group = self.asg['excavator']
        for sprite in pygame.sprite.spritecollide(self, excavator_group, False, pygame.sprite.collide_mask):
            # change ball direction
            self.direction.y = -1
            if sprite.rect.center[0] >= self.rect.x:
                self.direction.x = -1
                if check_key_pressed(pygame.K_LEFT) and self.excavator_data.rect.topleft[0] > FRAME_BLOCK_SIZE + 15:
                    self.rect.x -= ceil(self.excavator_data.velocity.x * randint(3, 9)) # change ball x_pos
            else:
                self.direction.x = 1
                if check_key_pressed(pygame.K_RIGHT) and self.excavator_data.rect.topright[0] < 440:
                    self.rect.x += ceil(self.excavator_data.velocity.x * randint(3, 9)) # change ball x_pos

    def check_if_level_complete(self):
        if not len(self.asg['tile']):  # check is all bricks were broken
            SCREEN.fill('black')
            background_image('./src/assets/images/backgrounds/bg_bonus.png', 50)
            self.excavator_data.points += 1000 * self.excavator_data.level # add bonus
            text_creator(f'BONUS - {1000 * self.excavator_data.level}', 'goldenrod4', S_W // 4 + 30, S_H // 2 - 20, 35, None, './src/fonts/born.ttf', True)
            Sound.stop_all_sounds()
            Sound.add_bonus_points(self)
            self.excavator_data.excavator_speed += 1.5
            if self.excavator_data.current_ball_speed < 4: # limit max ball speed
                self.excavator_data.current_ball_speed += 1
            self.excavator_data.lives += 1
            self.excavator_data.level += 1
            self.excavator_data.is_level_complete = True

    def reset_current_data(self):
        self.is_start_game = False
        self.is_start_game_timer = False
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = self.excavator_data.rect.midtop
        self.pos = vec(self.rect.midbottom)
        self.direction = vec(0, 0)
        self.speed = self.excavator_data.current_ball_speed


    def update(self):
        self.move()
        self.check_collide_in_wall()
        self.check_collide_in_tile()
        self.check_collide_in_excavator()
        self.check_if_level_complete()
        self.check_ball_in_frame_bug()