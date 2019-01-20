import random
from pygame.locals import Color
mass = 0.01
sayings = ["I'm best friends with Donald Trump!",
           "Its housewife, not househusband",
           "women in the workplace? ha.",
           "mwah ha ha ha haaaaa"]

def on_frame(self, key_state, level):
    if self.speech is None:
        self.say(random.choice(sayings), Color('purple'))
