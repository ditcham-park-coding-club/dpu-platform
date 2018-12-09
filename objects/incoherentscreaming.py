from pygame.locals import *
from setup import Physical

mass = 0.1
buoyancy = 11


def __init__(self):
    Physical.__init__(self)
    self.neep = False


def on_frame(self, key_state):
    if not self.neep:
        self.say('neep')
        self.neep = True
