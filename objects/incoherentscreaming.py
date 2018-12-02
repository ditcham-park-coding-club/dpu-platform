from pygame.locals import *

mass = 0.1


def on_frame(self, key_state):
    if not hasattr(self, 'neep'):
        self.say('neep')
        self.neep = True

def on_frame(self, key_state):
    if key_state[K_RIGHT]:
        self.dx = 5
    elif key_state[K_LEFT]:
        self.dx = -5

    if key_state[K_UP]:
        self.dy = -10

    if key_state[K_SPACE]:
        if self.hit is not None and hasattr(self.hit, 'action'):
            self.hit.action()
