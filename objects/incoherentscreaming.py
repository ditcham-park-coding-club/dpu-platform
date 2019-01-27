from pygame.locals import *
from setup import Physical

mass = 0.1

def on_frame(self, key_state, level):
    if key_state[K_RIGHT]:
        self.dx = 5
    elif key_state[K_LEFT]:
        self.dx = -5

    if key_state[K_UP]:
        self.dy = -10



def __init__(self):
    Physical.__init__(self)
    self.neep = False
