from src.settings import *


class Tile(pygame.sprite.Sprite):

    def __init__(self, x_pos=0, y_pos=0,):
        pygame.sprite.Sprite.__init__(self)
        self.random_brick_num = randint(1, 4)
        self.image = scale_image(f'./src/assets/images/tile/{self.random_brick_num}.png', 50, 30)
        self.rect = self.image.get_bounding_rect(min_alpha=1)
        self.rect.center = (x_pos, y_pos)





