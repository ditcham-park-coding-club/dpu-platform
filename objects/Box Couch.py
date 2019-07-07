import random

from setup import put

mass = 1
count_down = 100

# if things == []:

def action(self, level):
    self.kill()
    somethingType = random.choice(level.things)
    newThing = put(self.rect.x, self.rect.y, somethingType)
    newThing.moveable = False
    level.things.remove(somethingType)
    self.count_down = self.count_down - 1
    # Record what was found in the level
    level.last_found_furniture_type = newThing.type_name
