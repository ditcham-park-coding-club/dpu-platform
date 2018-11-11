from os import listdir, path
import importlib

import pygame
from pygame.locals import *

SCREEN_RECT = Rect(0, 0, 640, 480)
WIN_STYLE = 0  # |FULLSCREEN

AIR_RESISTANCE = 0.9

OBJECT_DEFAULTS = {
    'dx': 0.0,
    'dy': 0.0,
    'bounce': 0.3,
    'buoyancy': 0
}

pygame.init()
# Set the display mode
best_depth = pygame.display.mode_ok(SCREEN_RECT.size, WIN_STYLE, 32)
screen = pygame.display.set_mode(SCREEN_RECT.size, WIN_STYLE, best_depth)
pygame.display.set_caption('DPU Game')
pygame.mouse.set_visible(0)

background = pygame.Surface(SCREEN_RECT.size)

object_names = set([fn.rsplit('.', 1)[0] for fn in listdir('objects')])
object_types = {
    name: {
        **({'image': pygame.image.load(bmp).convert()} if path.exists(bmp) else {}),
        **(importlib.import_module('objects.' + name).__dict__ if path.exists('objects/%s.py' % name) else {})
    }
    for name, bmp in [(name, 'objects/%s.bmp' % name) for name in object_names]
}
all_group = pygame.sprite.RenderUpdates()


def put(x, y, object_type):
    sprite = pygame.sprite.Sprite(all_group)
    object_type = object_types[object_type]
    sprite.image = object_type['image']
    sprite.rect = sprite.image.get_rect(topleft=(x, y))
    # Set default values
    for key in OBJECT_DEFAULTS:
        setattr(sprite, key, object_type.get(key, OBJECT_DEFAULTS[key]))
