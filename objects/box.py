import random

from setup import put

mass = 1


def action(self):
    self.kill()
    put(self.rect.x, self.rect.y, random.choice(['balloon']))
