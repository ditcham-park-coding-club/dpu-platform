import random
from pygame.locals import Color

sayings = ["YA YEEEET",
           "Im just a pooor door i need no sympathy",
           "YEET!"]

def on_frame(self, key_state, level):
    if self.speech is None:
        self.say(random.choice(sayings))
