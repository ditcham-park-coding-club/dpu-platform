import random

from setup import put

mass = 1
count_down = 200
things = [ 'Bed']
#'Couch', 'Picture Of A Picture', 'Lamp GP', 'guineapigchair', 'tableandchair'
def action(self):
    self.kill()
    somethingType = random.choice(things)
    newThing = put(self.rect.x, self.rect.y, somethingType)
    newThing.moveable = False
    things.remove(somethingType)
    self.count_down = self.count_down - 1
    newThing.carrying.append(newThing)

    # Create a variable with a value of say 100, then make it smaller every frame.
    # To do this, you'll need an "on_frame" method. Read this:
    # https://github.com/ditcham-park-coding-club/dpu-platform/blob/master/objects/README.md#object-behaviour

#def on_frame(self, key_state, level):
    #when couch is found start countdown of 5 seconds
    #when countdow complete, change to Guineapighutch.py
    #when in Guineapighutch.py, let object be able to be moved
    #when object is in hutch level, remove from objects list
