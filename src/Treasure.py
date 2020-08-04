from Animation import Animation
from Text import Text

class Treasure(Animation):

    frames = ['img/chest_frame_1.png', 'img/chest_frame_2.png'] 

    def __init__(self, screen, pos):
        super().__init__(self.frames, pos, screen)
        self.reduce_scale(4)
        self.centralize()

        msg_pos = (pos[0], pos[1]+300)
        self.msg = Text(self.screen, msg_pos, 'Parabéns você encontrou o tesouro a tempo!', True, (255,255,255))

    def draw(self):
        super().draw()
        self.msg.draw()


