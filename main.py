import pygame.sprite

from src.settings import *
from src.classes.background import Background
from src.classes.sound import Sound
from src.classes.tile import Tile
from src.classes.excavator import Excavator
from src.classes.ball import Ball
from src.classes.table import Table

# ======================================================================== create Sprite groups

tile_group = pygame.sprite.Group()
excavator_group = pygame.sprite.GroupSingle()
ball_group = pygame.sprite.GroupSingle()
#
# # add to all_sprite_groups
all_spite_groups_dict = {'tile': tile_group, 'excavator': excavator_group, 'ball': ball_group}
#
# # ======================================================================= initialize  Classes
#
excavator = Excavator()
ball = Ball(all_spite_groups_dict, excavator)
#
# # add to group
excavator_group.add(excavator)
ball_group.add(Ball(all_spite_groups_dict, excavator))


# ==================================================================
table = Table(excavator)


# Game State
class GameState(Sound):
    COOLDOWN = 1000  # milliseconds
    start_timer = pygame.time.get_ticks()
    
    def __init__(self,):
        self.state = 'intro'
        self.background_frame = None
        self.background_picture = None
        self.start_game_counter = None
        self.is_wall_created = False
        self.is_music_play = False
        self.is_game_over = False
        self.reset_all_data_for_new_game = False


    def game(self):

        def wall_creator():
            for row in range(1, 7):
                for col in range(1, 12):
                    tile_group.add(Tile(50 * col + 7, 30 * row + 20))

        # ----------------------------- NEW GAME  reset all data
        if self.reset_all_data_for_new_game:
            self.background_frame = None
            self.background_picture = None
            self.start_game_counter = None
            self.is_wall_created = False
            self.is_music_play = False
            self.is_game_over = False
            self.reset_all_data_for_new_game = False
            ball.reset_current_data()
            excavator.reset_all_data()
            excavator.reset_current_data()
            all_spite_groups_dict['ball'].empty()
            ball_group.add(Ball(all_spite_groups_dict, excavator))
            ball.reset_current_data()
            tile_group.empty()


        # ----------------------------reset current game
        if excavator.is_lost_ball or excavator.is_level_complete:
            pygame.time.delay(2000)
            Sound.stop_all_sounds()
            # excavator.reset_current_data()
            self.start_game_counter = 3
            self.is_wall_created = False
            self.is_music_play = False
            excavator.reset_current_data()
            all_spite_groups_dict['ball'].empty()
            ball_group.add(Ball(all_spite_groups_dict, excavator))
            ball.reset_current_data()
            self.state = 'get_ready'

        if not self.is_wall_created:
            if not len(tile_group):
                wall_creator()
            Sound.background_music(self)
            self.background_frame =  Background('./src/assets/images/frames/frame.png')
            current_women = excavator.level
            if excavator.level > 9:
                current_women = 9
            scaled = scale_image(f'./src/assets/images/women/{current_women}.png', 550, 170)
            self.background_picture = Background(scaled, FRAME_BLOCK_SIZE + 5, FRAME_BLOCK_SIZE + 10, True)
            self.is_wall_created = True

        if excavator.is_pause:
            excavator.is_pause = False
            self.state = 'pause'

        if excavator.is_game_over:
            Sound.stop_all_sounds()
            Sound.game_over_music(self)
            self.state = 'game_over'

        # # =================================================== UPDATE
        # update BG
        self.background_frame.update()
        self.background_picture.update()
        table.update()


        # #  --------------------------- draw sprite group
        tile_group.draw(SCREEN)
        excavator_group.draw(SCREEN)
        ball_group.draw(SCREEN)
        # # --------------------------- update sprite group
        tile_group.update()
        excavator_group.update()
        ball_group.update()

        # excavator.update()

    def intro(self):
        if not self.is_music_play:
            Sound.intro_music(self)
            self.is_music_play = True
        font = './src/fonts/mario.ttf'
        background_image('./src/assets/images/backgrounds/bg_intro.png')
        text_creator('The hidden lady', 'brown1', 30, 220, 80, None, font )
        text_creator('(Breakout)', 'brown3', 230, 300, 50, None, font)
        text_creator('Menu - M', 'gold', S_W - 230, S_H - 160, 27, None, font)
        text_creator('Credits - C', 'fuchsia', S_W - 230, S_H - 110, 29, None, font)
        text_creator('Start game - SPACE', 'deepskyblue', S_W // 4 - 6, S_H - 24, 32, None, font)
        text_creator('By Abaddon', 'orange', 10, S_H - 10, 15, None, font)
        text_creator('Copyright ©2023', 'white', S_W - 150, S_H - 10, 15, None, font)

        if check_key_pressed(pygame.K_SPACE):
            Sound.btn_click(self)
            self.start_game_counter = 3
            Sound.stop_all_sounds()
            self.state = 'get_ready'
        if check_key_pressed(pygame.K_c):
            Sound.btn_click(self)
            self.state = 'credits'
        if check_key_pressed(pygame.K_m):
            Sound.btn_click(self)
            self.state = 'menu'
        exit_game()

    def menu(self):
        background_image('./src/assets/images/backgrounds/bg_menu.png')
        text_creator('Press RETURN to back...', 'cornsilk', S_W - 200, S_H - 10, 24)
        if check_key_pressed(pygame.K_RETURN):
            self.state = 'intro'
        exit_game()

    def credits(self):
        # background_image('./src/assets/images/backgrounds/bg_EMPTY.png')
        text_creator('CREDITS', 'slateblue3', S_W // 2 - 100, 40, 36, None, './src/fonts/born.ttf', True)
        text_creator('version: 1.0.0-beta', 'cornsilk', S_W - 130, 20, 20)

        text_creator('Free images:', 'brown', 110, 100, 35)
        text_creator('https://www.pngwing.com', 'cadetblue4', 130, 125, 30)

        text_creator('Free sounds:', 'brown', 110, 200, 35)
        text_creator('https://freesound.org/', 'cadetblue4', 130, 225, 30)

        text_creator('Platform 2D game:', 'brown', 110, S_H // 2, 34)
        text_creator('https://www.pygame.org', 'cadetblue4', 130, S_H // 2 + 24, 30)

        SCREEN.blit(pygame.image.load('./src/assets/images/title/pygame_logo.png'), (S_W // 4 - 50, S_H - 266))

        text_creator('Developer:', 'brown', 30, S_H - 60, 30)
        text_creator('by Abaddon', 'cadetblue4', 50, S_H - 40, 30)

        text_creator('Bug rapports:', 'brown', S_W // 2 - 90, S_H - 60, 30)
        text_creator('subtotal@abv.bg', 'cadetblue4', S_W // 2 - 70, S_H - 40, 30)

        text_creator('Copyright:', 'brown', S_W - 140, S_H - 60, 30)
        text_creator('© 2023', 'cadetblue4', S_W - 120, S_H - 40, 30)

        text_creator('Press RETURN to back...', 'cornsilk', S_W - 200, S_H - 10, 24)

        if check_key_pressed(pygame.K_RETURN):
            Sound.btn_click(self)
            self.state = 'intro'
        exit_game()

    def get_ready(self):
        time_now = pygame.time.get_ticks()
        if time_now - self.start_timer > self.COOLDOWN:
            self.start_game_counter -= 1
            self.start_timer = time_now
        background_image('./src/assets/images/backgrounds/bg_poster.png', 80, 10)
        text_creator('By Abaddon', 'orange', 10, S_H - 10, 15, None, './src/fonts/mario.ttf')
        text_creator('Copyright ©2023', 'brown', S_W - 150, S_H - 10, 15, None, './src/fonts/mario.ttf')
        text_creator(f'START AFTER: {self.start_game_counter}', 'purple', 215, S_H - 40, 40, None, './src/fonts/mario.ttf')

        if self.start_game_counter == 0:
            excavator.is_lost_ball = False
            excavator.is_level_complete = False
            self.state = 'game'
        exit_game()

    def start_pause(self):
        background_image('./src/assets/images/backgrounds/bg_pause.png')
        text_creator('PAUSE', 'red3', S_W // 2, S_H  // 2 - 30, 80, None, './src/fonts/born.ttf')
        text_creator('Press RETURN to continue...', 'bisque', S_W - 245, S_H - 12)

        if key_pressed(pygame.K_RETURN):
            self.state = 'game'

    def game_over(self):

        background_image('./src/assets/images/backgrounds/bg_game_over.png')
        text_creator('Press RETURN to back...', 'darkblue', S_W - 200, S_H - 10, 26)

        if key_pressed(pygame.K_RETURN):
            Sound.stop_all_sounds()
            Sound.intro_music(self)
            self.reset_all_data_for_new_game = True
            self.state = 'intro'
        exit_game()

    # ========================================= state manager ...
    def state_manager(self):
        # print(self.state)
        if self.state == 'intro':
            self.intro()
        if self.state == 'game':
            self.game()
        if self.state == 'get_ready':
            self.get_ready()
        if self.state == 'menu':
            self.menu()
        if self.state == 'credits':
            self.credits()
        if self.state == 'pause':
            self.start_pause()
        if self.state == 'game_over':
            self.game_over()


#  ================================ create new GameState
game_state = GameState()


# ============= Starting Game loop
while True:
    SCREEN.fill(pygame.Color('black'))
    game_state.state_manager()
    pygame.display.update()
    CLOCK.tick(FPS)
    exit_game()
