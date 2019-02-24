# Make self.hit_by
import random

is_random = False

count = 0

def on_frame(self, key_state, level):
    if self.is_random:
        self.dx = random.choice([-10, 10])
    else:
        count = count + 1
        if self.count = 10:
            self.dx = -10
