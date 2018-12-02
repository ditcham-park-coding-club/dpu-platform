from importlib import import_module
from math import log10
from os import listdir, path

import pygame
from pygame.locals import *

FRAME_RATE = 40
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
        self.rect = None
        (self.dx, self.dy) = (0.0, 0.0)
        self.carrying = []
        index = sum(1 for s in object_group.sprites() if type(s).__name__ == type(self).__name__)
        self.name = f"{type(self).__name__}{index}"
        self.speech = None

    def __str__(self):
        return self.name

    # noinspection PyStatementEffect,PyUnusedLocal,PyMethodMayBeStatic
    def on_frame(self, *args):
        None

    def update(self, *args):
        if self.speech is not None and not self.speech.alive():
            self.speech = None

    def say(self, msg, color=Color('white')):
        if self.speech is not None:
            self.speech.kill()
        self.speech = Speech(self, msg, color)


class Speech(pygame.sprite.Sprite):
    def __init__(self, speaker, msg, color=Color('white')):
        super().__init__(all_group)
        self.speaker = speaker
        self.font = pygame.font.Font(None, 25)
        self.life = FRAME_RATE * log10(len(msg))
        self.image = self.font.render(msg, 0, color)
        self.rect = self.image.get_rect()
        self._align()

    def _align(self):
        self.rect.center = self.speaker.rect.center
        space = first(r for r in outside_rects(self.speaker.rect) if fits(self.rect, r))
        if space is not None:
            self.rect.clamp_ip(space)

    def update(self, *args):
        self.life = self.life - 1
        if self.life <= 0:
            self.kill()
        else:
            self._align()


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


def put(x, y, object_type_name, object_name=None):
    object_type = object_types[object_type_name]
    sprite = object_type()
    sprite.add(all_group, object_group)

    sprite.rect = sprite.image.get_rect(topleft=(x, y))
    if object_name is not None:
        sprite.name = object_name

    if not SCREEN_RECT.contains(sprite.rect):
        sprite.rect.clamp_ip(SCREEN_RECT)
        log(1, f"{sprite.name} was not on the screen, moved to {sprite.rect.x, sprite.rect.y}")

    choose_next = ChooseNext()
    c = first(all_collisions(sprite))
    while c:
        sprite.rect.clamp_ip(choose_next.choice(list(r for r in outside_rects(c.rect) if fits(sprite.rect, r))))
        c = first(all_collisions(sprite))
    if choose_next.chosen():
        log(1, f"{sprite.name} overlapped with other sprites, moved to {sprite.rect.x, sprite.rect.y}")


object_names = set([fn.rsplit('.', 1)[0] for fn in listdir('objects')])
object_types = {
    name: type(name, (Physical,), {
        **({'image': load_image(name)} if path.exists(image_path(name)) else {}),
        **({k: v for k, v in import_module(f"objects.{name}").__dict__.items() if not k.startswith('__')}
           if path.exists(f"objects/{name}.py") else {})
    })
    for name in object_names
}
all_group = pygame.sprite.RenderUpdates()

object_group = pygame.sprite.Group()

for key in object_types:
    if hasattr(object_types[key], 'image'):
        image = object_types[key].image
        if image is not None:
            log(1, f"{key} has dimensions {image.get_width(), image.get_height()}")


class ChooseNext(object):
    def __init__(self):
        self.index = -1

    def choice(self, seq):
        self.index = self.index + 1
        return seq[self.index % len(seq)]

    def chosen(self):
        return self.index > -1


def all_collisions(sprite):
    for c in pygame.sprite.spritecollide(sprite, object_group, False):
        if c is not sprite:
            yield c


def first(gen):
    for item in gen:
        return item
    return None


def outside_rects(rect):
    outside = SCREEN_RECT.copy()
    outside.height = rect.top - SCREEN_RECT.top
    outside.bottom = rect.top
    yield outside
    outside = SCREEN_RECT.copy()
    outside.width = SCREEN_RECT.right - rect.right
    outside.left = rect.right
    yield outside
    outside = SCREEN_RECT.copy()
    outside.height = SCREEN_RECT.bottom - rect.bottom
    outside.top = rect.bottom
    yield outside
    outside = SCREEN_RECT.copy()
    outside.width = rect.left - SCREEN_RECT.left
    outside.right = rect.left
    yield outside


def fits(r: Rect, into: Rect):
    return into.width >= r.width and into.height >= r.height
