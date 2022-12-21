from src.settings import text_creator, START_FRAME_SIZE, CLOCK


class Table:
    def __init__(self, excavator):
        self.excavator_data = excavator
        self.height_score = 10000

    def draw_labels_and_table_data(self):
        # label height_score
        x_pos = START_FRAME_SIZE + 50
        sec_x_pos = START_FRAME_SIZE + 60
        font_size = 18
        sec_font_size = 20
        font = './src/fonts/aAblasco.ttf'

         # label top score
        text_creator('Top Score', 'crimson', x_pos, 60, font_size, None, font, True)
        if self.excavator_data.points >= self.height_score:
            self.height_score = self.excavator_data.points
        text_creator(f'{self.height_score}', 'crimson', sec_x_pos, 90, sec_font_size, None, font,)

        # label_score
        text_creator('You Score', 'cornflowerblue',  x_pos, 140, font_size, None, font, True)
        text_creator(f'{self.excavator_data.points}', 'cornflowerblue', sec_x_pos, 170, sec_font_size, None, font)
        #
        #
        # label lives
        text_creator('Lives', 'springgreen4', x_pos, 210, font_size, None, font, True)
        text_creator(f'{self.excavator_data.lives}', 'springgreen4', sec_x_pos, 240, sec_font_size, None, font)

        # # label level
        text_creator('Level', 'orange', x_pos, 280, font_size, None, font, True)
        text_creator(f'{self.excavator_data.level}', 'orange', sec_x_pos , 310, sec_font_size, None, font)
        #
        # label broken bricks
        text_creator('Broken Bricks', 'deepskyblue4', x_pos , 350, font_size , None, font, True)
        text_creator(f'{self.excavator_data.counter_broken_bricks}', 'deepskyblue4', sec_x_pos, 380, sec_font_size, None, font)

        # # play time
        text_creator('Play Time', 'purple', x_pos, 420, font_size, None, font, True)
        if self.excavator_data.seconds < 10:
            text_creator(f'{self.excavator_data.minutes} : 0{self.excavator_data.seconds}', 'white', sec_x_pos, 450, sec_font_size, None, font)
        else:
            text_creator(f'{self.excavator_data.minutes} : {self.excavator_data.seconds}', 'white', sec_x_pos, 450, sec_font_size, None, font)

         # # label FPS
        text_creator(f'Current FPS', 'grey49', x_pos, 490, font_size, None, font, True)

        text_creator(f'{int(CLOCK.get_fps())}', 'grey49', sec_x_pos, 520, font_size, None, font)


    def update(self):
        self.draw_labels_and_table_data()





