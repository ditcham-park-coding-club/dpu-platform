from pygame.locals import *

sayings = ["Hi!",
           "Your object is to release all the balloons"]


def on_frame(self, key_state):
    if key_state[K_RIGHT]:
        self.dx = 5
    elif key_state[K_LEFT]:
        self.dx = -5

    if key_state[K_UP]:
        self.dy = -10

    if key_state[K_SPACE]:
        if self.hit is not None:
            self.hit.action()

    if sayings and self.speech is None:
        self.say(sayings.pop(0))
