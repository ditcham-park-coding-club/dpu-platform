import random
from pygame.locals import Color
mass = 0.01
sayings = ["Grrr",
           "Don't do drugs kids!(or do)",
           "These should keep me entertained for a while....",
           "My unmarked white van does not have a numberplate"]

def on_frame(self, key_state, level):
    if self.speech is None:
        self.say(random.choice(sayings), Color('purple'))
