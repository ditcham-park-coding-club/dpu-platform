import random
from pygame.locals import Color

mass = 0.01
sayings = ["Hello", "My name is Pumpkin", "Help Fudge to open the boxes and decorate her new hutch"]

def on_frame(self, key_state, level):
    if self.speech is None:
        self.say(random.choice(sayings), Color('purple'))
