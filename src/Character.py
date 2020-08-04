from Animation import Animation

class Character(Animation):

    masc = ["img/pirate_frame1.png", "img/pirate_frame2.png"]
    fem = ["img/girlpirate_frame1.png", "img/girlpirate_frame2.png"]

    def __init__(self, screen, sex, block):

        if sex == 0:
            super().__init__(self.fem, block.center, screen)
            # self.frames = self.fem
        else:
            super().__init__(self.masc, block.center, screen)
            # self.frames = self.masc

        self.chances = 3
        self.dir = 1
        self.block = block
        self.x = self.block.center[0]
        self.y = self.block.center[1]
        self.update_pos((self.x, self.y))

    def update_block(self, block):
        self.block = block
        self.lerp = True
        self.update_pos(self.block.center)

    def update_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1] - 100
        self.update_rect()

    def flip(self):
        super().flip()
        self.dir += 1
        self.dir = self.dir % 2

    def dig(self):
        return self.block.value


        
