import random
from pygame.locals import Color
mass=0.1
sayings = ["Grrr",
           "Circular people go home",
           "NO immigration",
           "mwah ha ha ha haaaaa"]

def on_frame(self, key_state):
    if self.speech is None:
        self.say(random.choice(sayings), Color('purple'))