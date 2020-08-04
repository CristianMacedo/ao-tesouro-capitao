import pygame

class Text:

    font = './font/oh-whale.ttf'
    fontsize = 30

    def __init__(self, screen, pos, text, bg_active=False, bgcolor=(0,0,0), fontsize=fontsize):

        self.text = " " + text + " "
        self.screen = screen
        self.bg_active = bg_active

        pygame.font.init()
        self.loaded_font = pygame.font.Font(self.font, fontsize)
        self.textsurface = self.loaded_font.render(self.text, False, (0, 0, 0))
        self.pos = (pos[0] - self.textsurface.get_width()/2, pos[1] - self.textsurface.get_height()/2)

        if(self.bg_active):
            self.bg = pygame.Surface((self.textsurface.get_width(),self.textsurface.get_height()))
            self.bg.fill(bgcolor) 


    def draw(self):

        if(self.bg_active):
            self.screen.blit(self.bg,self.pos)

        self.screen.blit(self.textsurface,self.pos)
