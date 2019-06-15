from pygame.locals import *

sayings = ["Hi!",
            "I'm a happinator.",
            "That means I make people who feel unhappy...",
            "Happy again!!",
            "Help me on my quest for happiness.",
            "And remember...",
            "Nothing cheers people up like balloons!"]

def on_frame(self, key_state, level):
    if key_state[K_RIGHT]:
        self.dx = 5
    elif key_state[K_LEFT]:
        self.dx = -5

    if key_state[K_UP]:
        self.dy = -10

    if key_state[K_SPACE]:
        if self.hit is not None:
            self.hit.action(level)

    if sayings and self.speech is None:
        self.say(sayings.pop(0))
