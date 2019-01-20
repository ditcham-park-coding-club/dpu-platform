import random

from setup import put

mass = 1

def action(self):
    self.kill()
    # random.choice(['Couch']) is making a random choice from a list of one thing. You could just have 'Couch'.
    put(self.rect.x, self.rect.y, random.choice(['Couch']))
    #i want to wait for a bit then move to the hutch scene and position the Couch
    # OK. To wait for a bit, how about doing a countdown?
    # Create a variable with a value of say 100, then make it smaller every frame.
    # To do this, you'll need an "on_frame" method. Read this:
    # https://github.com/ditcham-park-coding-club/dpu-platform/blob/master/objects/README.md#object-behaviour
    # What is the "hutch scene"? Is that another level? If so, when the countdown
    # gets to zero, we need to complete the level. Have a go at something and I'll help!
