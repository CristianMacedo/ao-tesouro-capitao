import pygame

class Overlay:

    alpha = 128
    color = (0,0,0)

    def __init__(self, screen, pos, width, height):

        self.screen = screen
        self.pos = pos
        self.overlay = pygame.Surface((width,height))
        self.overlay.set_alpha(self.alpha)
        self.overlay.fill(self.color) 
    
    def draw(self):

        self.screen.blit(self.overlay,self.pos)