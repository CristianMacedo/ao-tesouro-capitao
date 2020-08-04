from Button import Button
import pygame

# This class is responsible for managing the buttons available on the main menu
# It receives the amount of buttons to redistribute all of them accross its size

class Menu:

    def __init__(self, screen):
        self.buttons = {}
        self.screen = screen
        self.last_clicked_state = None

    def add_button(self, btn_name, frames, pos, next_state):
        # Adding the given button to the buttons array and distaciating it
        # according to the previously calculated `height diff`
        button = Button(frames, pos, self.screen, next_state)
        self.buttons[btn_name] = button

    def draw(self):
        # Check menu size drawing a rectangle on its coordenates
        # pygame.draw.rect(self.screen, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)

        # Calling the draw() function for each button
        for button in self.buttons.values():
            button.draw()

    def check_click(self, click_pos):
        # Checking if the given mouse click position is inside one of the
        # button rectangle area, and calling its callback if this is true
        for button in self.buttons.values():
            if button.rect.collidepoint(click_pos):
                self.last_clicked_state = button.next_state  
                return True



