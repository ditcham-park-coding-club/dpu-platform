import random
from pygame.locals import Color
mass = 0.01
sayings = ["You peasant",
           "im the bestest in all the world",
           "I deserve to be the king because i can sing a C sharp!",
           "mwah ha ha ha haaaaa"]

def on_frame(self, key_state, level):
    if self.speech is None:
        self.say(random.choice(sayings), Color('purple'))
