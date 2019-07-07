from pygame.locals import *

moveable = True
buoyancy = 10

def on_frame(self, key_state, level):
    if self.moveable:

        if key_state[K_RIGHT]:
            self.dx = 5
        elif key_state[K_LEFT]:
            self.dx = -5
        elif key_state[K_UP]:
            self.dy = -10
        elif key_state[K_DOWN]:
            self.dy = 10
        else:
            # Circumvent annoying momentum
            self.dx = self.dy = 0

        if key_state[K_SPACE]:
            self.moveable = False
