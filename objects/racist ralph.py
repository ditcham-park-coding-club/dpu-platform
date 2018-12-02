import random
from pygame.locals import Color

sayings = ["Grrr",
           "Circular people go home",
           "NO immigration",
           "I want a cupcake",
           "saleha started it",
           "mwah ha ha ha haaaaa"]

def on_frame(self, key_state):
    if self.speech is None:
        self.say(random.choice(sayings), Color('purple'))
