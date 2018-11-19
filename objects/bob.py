from pygame.locals import *


def on_key(self, key_state):
    if key_state[K_RIGHT]:
        self.dx = 5
    elif key_state[K_LEFT]:
        self.dx = -5

    if key_state[K_UP]:
        self.dy = -30

    if key_state[K_SPACE] and self.hit is not None:
        if type(self.hit).__name__ == 'box':
            self.hit.explode()

