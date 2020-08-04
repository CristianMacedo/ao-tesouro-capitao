import pygame

# This class is made to control an animated object
# it receives one array with file paths,
# It swaps through each of the images according to the predefined fps

class Animation():

    # Swaping speed (fps = n, the images will be swaped every n frames)
    fps = 15

    def __init__(self, frames, pos, screen):

        if(isinstance(frames, dict)):
            self.states = frames.copy()
            frames = list(self.states.values())[0]
            for state in self.states:
                self.states[state] = self.load_frames(self.states[state])

        else:
            self.states = None

        self.screen = screen
        self.frames = self.load_frames(frames)
        self.frame_counter = 0
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    @staticmethod
    def load_frames(frames):
        loaded = []
        for frame in frames:
            loaded.append(pygame.image.load(frame))
        return loaded

    def switch_state(self, state_name):
        self.frames = self.states[state_name] 
        self.swap_frame()
        self.update_rect()           

    # Bliting the animation on the given screen
    def draw(self):
        if self.frame_counter%self.fps == 0:
            self.frame_index += 1
            self.swap_frame()

        self.screen.blit(self.image, (self.rect.x, self.rect.y))
        self.frame_counter += 1

    def update_pos(self, pos):
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.update_rect()

    def update_rect(self):
        aux_x = self.rect.x
        aux_y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = aux_x
        self.rect.y = aux_y

    def flip(self):
        

        if(self.states):
            for state in self.states:
                aux = []
                for frame in self.states[state]:
                    new_img = pygame.transform.flip(frame, True, False)
                    aux.append(new_img)
                self.states[state] = aux

        aux = []
        for frame in self.frames:
            new_img = pygame.transform.flip(frame, True, False)
            aux.append(new_img)

        self.frames = aux
        self.swap_frame()
        self.update_rect()

    def centralize(self):
        self.rect.x -= self.rect.width/2
        self.rect.y -= self.rect.height/2

    def reduce_scale(self, scale_factor):

        if(self.states):
            for state in self.states:
                aux = []
                for frame in self.states[state]:
                    new_img = pygame.transform.scale(frame, (int(self.rect.width/scale_factor), int(self.rect.height/scale_factor)))
                    aux.append(new_img)
                self.states[state] = aux

        aux = []
        for frame in self.frames:
            new_img = pygame.transform.scale(frame, (int(self.rect.width/scale_factor), int(self.rect.height/scale_factor)))
            aux.append(new_img)

        self.frames = aux
        self.swap_frame()
        self.update_rect()

    def set_fps(self, fps):
        self.fps = fps

    # Swaps to the next frame according to the frame controler
    # frame_index can go up to the frames array length using the % (module)
    # If the frame array has 3 frames the calculation will be (0...n) % 3 and the possible values will be 0, 1 and 2
    def swap_frame(self):
        self.image = self.frames[self.frame_index%len(self.frames)]
