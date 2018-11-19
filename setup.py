from os import listdir, path
import importlib

import pygame
from pygame.locals import *

SCREEN_RECT = Rect(0, 0, 640, 480)
WIN_STYLE = 0  # |FULLSCREEN

AIR_RESISTANCE = 0.9


class Physical(pygame.sprite.Sprite):
    mass = 10.0
    elasticity = 0.3
    buoyancy = 0.0

    def __init__(self, *groups):
        super().__init__(*groups)
        self.dx = self.dy = 0.0
        self.carrying = []

    # noinspection PyStatementEffect,PyUnusedLocal,PyMethodMayBeStatic
    def on_key(self, *args):
        None


pygame.init()
# Set the display mode
best_depth = pygame.display.mode_ok(SCREEN_RECT.size, WIN_STYLE, 32)
screen = pygame.display.set_mode(SCREEN_RECT.size, WIN_STYLE, best_depth)
pygame.display.set_caption('DPU Game')

background = pygame.Surface(SCREEN_RECT.size)

object_names = set([fn.rsplit('.', 1)[0] for fn in listdir('objects')])
object_types = {
    name: type(name, (Physical,), {
        **({'image': pygame.image.load(bmp).convert()} if path.exists(bmp) else {}),
        **({k: v for k, v in importlib.import_module(f"objects.{name}").__dict__.items() if not k.startswith('__')}
           if path.exists(f"objects/{name}.py") else {})
    })
    for name, bmp in [(name, f"objects/{name}.bmp") for name in object_names]
}
all_group = pygame.sprite.RenderUpdates()

for key in object_types:
    if hasattr(object_types[key], 'image'):
        image = object_types[key].image
        if image is not None:
            print(f"{key} has dimensions {image.get_width(), image.get_height()}")


def put(x, y, object_type_name, object_name=None):
    object_type = object_types[object_type_name]
    sprite = object_type()
    all_group.add(sprite)
    sprite.rect = sprite.image.get_rect(topleft=(x, y))
    sprite.name = object_name if object_name is not None else \
        object_type_name + str(sum([1 for s in all_group.sprites() if type(s).__name__ == object_type_name]))
