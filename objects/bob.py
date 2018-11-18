from pygame.locals import *


def on_key(self, key_state):
    if key_state[K_RIGHT]:
        self.dx = 5
    elif key_state[K_LEFT]:
        self.dx = -5

    if key_state[K_UP]:
        self.dy = -30

    if key_state[K_SPACE] and self.touching is not None:
        touch = self.touching
        if type(touch).__name__ == 'box':
            touch.explode()

