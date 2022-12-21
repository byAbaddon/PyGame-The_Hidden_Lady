import pygame
pygame.mixer.init()
pygame.mixer.pre_init(44100, -16, 2, 2048)


class Sound:
    @staticmethod
    def play_sound(sound_file, volume=0.5, loops=0):
        play = pygame.mixer.Sound(sound_file)
        play.set_volume(volume)
        play.play(loops)

    @staticmethod
    def stop_all_sounds():
        pygame.mixer.stop()

    def btn_click(self):
        self.play_sound('./src/assets/sounds/btn_one.wav')

    # Background
    def intro_music(self):
        self.play_sound('./src/assets/sounds/intro_music.mp3', 0.6, -1)

    def background_music(self):
        self.play_sound('./src/assets/sounds/background_one.mp3', 0.6, -1)

    def game_over_music(self):
        self.play_sound('./src/assets/sounds/game_over_music.mp3', 0.6, -1)

    def bonus_music(self):
        self.play_sound('./src/assets/sounds/bonus_music.mp3', 0.8, - 1)


    # ------------------------------------------------------
    def engin(self):
        self.play_sound('./src/assets/sounds/engin.wav', 0.1)

    def break_brick(self):
        self.play_sound('./src/assets/sounds/break_brick_2.wav', 0.8)

    def add_bonus_points(self):
        self.play_sound('./src/assets/sounds/add_bonus_points.wav')

    def lost_ball(self):
        self.play_sound('./src/assets/sounds/lost_ball.wav' )