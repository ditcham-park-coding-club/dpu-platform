import random

from setup import put

mass = 1
count = 200

def action(self):
    self.kill()
    put(self.rect.x, self.rect.y, random.choice(['Couch', 'Picture Of A Picture', 'Lamp GP', 'guineapigchair', 'Bed', 'tableandchair']))
    self.count = self.count - 1

    # Create a variable with a value of say 100, then make it smaller every frame.
    # To do this, you'll need an "on_frame" method. Read this:
    # https://github.com/ditcham-park-coding-club/dpu-platform/blob/master/objects/README.md#object-behaviour

#def on_frame(self, key_state, level):
    #when couch is found start countdown of 5 seconds
    #when countdow complete, change to Guineapighutch.py
    #when in Guineapighutch.py, let object be able to be moved
    #when object is in hutch level, remove from objects list
