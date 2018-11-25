from pygame.locals import *

sayings = ["Hi!",
           "My name is Bob",
           "Move me with the LEFT and RIGHT keys",
           "Jump me with the UP key",
           "Press SPACE to do something"]


def on_frame(self, key_state):
    if key_state[K_RIGHT]:
        self.dx = 5
    elif key_state[K_LEFT]:
        self.dx = -5

    if key_state[K_UP]:
        self.dy = -20

    if key_state[K_SPACE]:
        if self.hit is not None and hasattr(self.hit, 'action'):
            self.hit.action()

    if sayings and self.speech is None:
        self.say(sayings.pop(0))
