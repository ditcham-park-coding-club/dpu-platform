import importlib
import random
from os import listdir, path

import pygame
from pygame.locals import *

SCREEN_RECT = Rect(0, 0, 640, 480)
WIN_STYLE = 0  # |FULLSCREEN
AIR_RESISTANCE = 0.9
LOG_LEVEL = 1


def log(level, string):
    if level <= LOG_LEVEL:
        print(string)


class Physical(pygame.sprite.Sprite):
    mass = 10.0
    elasticity = 0.3
    buoyancy = 0.0

    def __init__(self, *groups):
        super().__init__(*groups)
        (self.dx, self.dy) = (0.0, 0.0)
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


def image_path(name):
    return f"objects/{name}.bmp"


def load_image(name):
    return pygame.image.load(image_path(name)).convert()


object_names = set([fn.rsplit('.', 1)[0] for fn in listdir('objects')])
object_types = {
    name: type(name, (Physical,), {
        **({'image': load_image(name)} if path.exists(image_path(name)) else {}),
        **({k: v for k, v in importlib.import_module(f"objects.{name}").__dict__.items() if not k.startswith('__')}
           if path.exists(f"objects/{name}.py") else {})
    })
    for name in object_names
}
all_group = pygame.sprite.RenderUpdates()

for key in object_types:
    if hasattr(object_types[key], 'image'):
        image = object_types[key].image
        if image is not None:
            log(1, f"{key} has dimensions {image.get_width(), image.get_height()}")


def put(x, y, object_type_name, object_name=None):
    object_type = object_types[object_type_name]
    sprite = object_type()
    all_group.add(sprite)
    sprite.rect = sprite.image.get_rect(topleft=(x, y))
    sprite.name = object_name if object_name is not None else \
        object_type_name + str(sum([1 for s in all_group.sprites() if type(s).__name__ == object_type_name]))

    if not SCREEN_RECT.contains(sprite.rect):
        sprite.rect.clamp_ip(SCREEN_RECT)
        log(1, f"{sprite.name} was not on the screen, moved to {sprite.rect.x, sprite.rect.y}")

    warn = False
    c = first(all_collisions(sprite))
    while c:
        warn = True
        sprite.rect.clamp_ip(random.choice(list(r for r in outside_rects(c.rect)
                                                if r.width >= sprite.rect.width and r.height >= sprite.rect.height)))
        c = first(all_collisions(sprite))
    if warn:
        log(1, f"{sprite.name} overlapped with other sprites, moved to {sprite.rect.x, sprite.rect.y}")


def all_collisions(sprite):
    for c in pygame.sprite.spritecollide(sprite, all_group, False):
        if c is not sprite:
            yield c


def first(gen):
    for item in gen:
        return item
    return None


def outside_rects(rect):
    outside = SCREEN_RECT.copy()
    outside.right = rect.left
    yield outside
    outside = SCREEN_RECT.copy()
    outside.bottom = rect.top
    yield outside
    outside = SCREEN_RECT.copy()
    outside.left = rect.right
    yield outside
    outside = SCREEN_RECT.copy()
    outside.top = rect.bottom
    yield outside
