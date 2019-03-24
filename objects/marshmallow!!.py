import random
from pygame.locals import Color

mass = 0.01
sayings = ["Hello", "My name is Marshmallo", "Click the space bar to open the boxes"]

def on_frame(self, key_state, level):
    if self.speech is None:
        self.say(random.choice(sayings), Color('red'))
