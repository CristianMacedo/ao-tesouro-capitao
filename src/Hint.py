import pygame
from Animation import Animation
from Text import Text
from Overlay import Overlay

class Hint:

    scrol_frames = ['img/scrol_frame_1.png','img/scrol_frame_2.png']

    def __init__(self, pos, hint, screen):
        
        self.pos = pos
        self.hint = hint
        self.screen = screen
    
        self.overlay = Overlay(self.screen, (0, 0), self.screen.get_size()[0], self.screen.get_size()[1])
        self.textsurface = Text(self.screen, self.pos, self.hint, True, (232,197,150))

        self.scrol = Animation(self.scrol_frames, self.pos, self.screen)
        self.scrol.reduce_scale(4)
        self.scrol.centralize()

        self.elements = [self.overlay, self.scrol, self.textsurface]

    def draw(self):

        for element in self.elements:
            element.draw()
