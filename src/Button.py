from Animation import Animation

# This class is responsible of containing the button information
# and storing a callback to be activated once the `click` function is called

class Button(Animation):

    def __init__(self, frames, pos, screen, next_state):

        # Giving the needed attributes to the super class constructor (Animation)
        super().__init__(frames, pos, screen)
        self.next_state = next_state
