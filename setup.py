from os import listdir, path

import pygame
from pygame.locals import *

SCREEN_RECT = Rect(0, 0, 640, 480)
WIN_STYLE = 0  # |FULLSCREEN

AIR_RESISTANCE = 0.9

pygame.init()
# Set the display mode
best_depth = pygame.display.mode_ok(SCREEN_RECT.size, WIN_STYLE, 32)
screen = pygame.display.set_mode(SCREEN_RECT.size, WIN_STYLE, best_depth)
pygame.display.set_caption('DPU Game')
pygame.mouse.set_visible(0)

background = pygame.Surface(SCREEN_RECT.size)

object_names = set([fn.rsplit('.', 1)[0] for fn in listdir('objects')])
object_types = {
    name: pygame.image.load(bmp).convert()
    for name, bmp in [(name, 'objects/' + name + '.bmp') for name in object_names]
    if path.exists(bmp)
}
all_group = pygame.sprite.RenderUpdates()


def put(x, y, object_type):
    sprite = pygame.sprite.Sprite(all_group)
    sprite.image = object_types[object_type]
    sprite.rect = sprite.image.get_rect(topleft=(x, y))
    sprite.dx = 0.0
    sprite.dy = 0.0
    sprite.bounce = 0.3
