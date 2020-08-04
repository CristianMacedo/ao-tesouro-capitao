import pygame

class Block:
    def __init__(self, x, y, width, height, screen, matrix_pos, value):
        self.screen = screen
        self.color = (0, 0, 0)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.matrix_pos = matrix_pos
        self.center = (self.x + (self.width/2), self.y + (self.height/2))
        self.value = value

    # RETURN X AXIS
    def getX(self):
        return self.x

    # RETURN Y AXIS
    def getY(self):
        return self.y

    # DEFINE X AXIS
    def setX(self, x):
        self.x = x

    # DEFINE Y AXIS
    def setY(self, y):
        self.y = y

    def draw(self):
        return pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height), 1)
