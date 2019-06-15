import random

from setup import put

mass = 9999


def action(self, level):
    self.kill()
    put(self.rect.x, self.rect.y, random.choice(['balloon']))
