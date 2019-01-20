import random
from pygame.locals import Color
mass = 0.01
sayings = ["Its Adam and Eve not Adam and Steve.",
           "#the-catholic-church-is-my-bae",
           "Im hungry..... but not for justice. for food. like a normal person.",
           "mwah ha ha ha haaaaa"]

def on_frame(self, key_state, level):
    if self.speech is None:
        self.say(random.choice(sayings), Color('purple'))
