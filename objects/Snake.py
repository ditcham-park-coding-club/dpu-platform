# Make self.hit_by
import random

is_random = False

going_left = True

def on_frame(self, key_state, level):
    if self.is_random:
        self.dx = random.choice([-10, 10])
    else:
        if self.hit is not None:
            if self.going_left == True:
                self.going_left = False
            elif self.going_left == False:
                self.going_left = True

        #self.count = self.count + 1
        if self.going_left:
            self.dx = -2
        else:
            self.dx = 2
