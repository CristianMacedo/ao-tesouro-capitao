from Block import Block
from Treasure import Treasure
from Hint import Hint
from Text import Text
import random
import math

class Map: 

    def __init__(self, col, screen, w, h):
        self.first_hint = None
        self.blocks = []
        self.treasure_index = None
        self.hint_index = None
        self.w = w
        self.h = h
        self.screen = screen
        self.col = col
        self.row = 3
        self.create_map()

    @staticmethod
    def return_dist(pos1, pos2):

        x_off = pos2[0] - pos1[0]
        y_off = pos2[1] - pos1[1]

        return (x_off, y_off)

    def create_map(self):

        block_w = self.w/self.col
        block_h = self.h/2

        empty_field_msg =  Text(self.screen, (int(self.w/2), 200), 'Este campo está vazio', True, (255,255,255))

        lastX = 0
        lastY = block_h

        # MAP OBJECTS
        for x in range(self.row):
            for y in range(self.col):
                self.blocks.append(Block(lastX, lastY, block_w, block_h/3, self.screen, (x, y), empty_field_msg))
                lastX += block_w
            lastY += block_h/3
            lastX = 0

        self.treasure_index = random.randint(1, len(self.blocks)-1)
        self.blocks[self.treasure_index].value = Treasure(self.screen, (int(self.w/2), 200))
        print('Tesouro: {}'.format(self.treasure_index))
        
        self.hint_index = random.randint(1, len(self.blocks)-1)
        while (self.hint_index == self.treasure_index):
            self.hint_index = random.randint(1, len(self.blocks)-1)
        print('Dica: {}'.format(self.hint_index))

        dist = self.return_dist(self.blocks[self.hint_index].matrix_pos, self.blocks[self.treasure_index].matrix_pos)
        hint_str = self.create_hint_text('O tesouro', dist)

        self.blocks[self.hint_index].value = Hint((int(self.w/2), 200), hint_str, self.screen)
        print('O texto da dica é '+ hint_str)

        first_hint_dist = self.blocks[self.hint_index].matrix_pos
        first_hint_str = self.create_hint_text('A dica', first_hint_dist)

        self.first_hint = Hint((int(self.w/2), 200), first_hint_str, self.screen)

    @staticmethod
    def create_hint_text(el_name, dist):

        if (dist[0] < 0):
            y_dir = 'cima'
        else:
            y_dir = 'baixo'

        if (dist[1] < 0):
            x_dir = 'esquerda'
        else:
            x_dir = 'direita'

        return "{} está a {} passos a {} e {} passos a {}".format(el_name, abs(dist[0]), y_dir, abs(dist[1]), x_dir)

    def draw(self):

        for block in self.blocks:
            block.draw()
