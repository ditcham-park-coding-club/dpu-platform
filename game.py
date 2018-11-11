import runpy
import sys
import math

import pygame
from pygame.locals import *

from setup import all_group, screen, SCREEN_RECT, background, AIR_RESISTANCE


def main():
    # Run the requested level
    runpy.run_module("levels." + sys.argv[1])

    clock = pygame.time.Clock()

    while not has_quit():
        all_group.clear(screen, background)

        # Apply velocity
        for sprite in all_group:
            sprite.rect.move_ip(sprite.dx, sprite.dy)

        # Resolve collisions with the walls
        for sprite in all_group:
            resolve_wall_collision(sprite)

        # Resolve collisions with other sprites
        dirty_group = all_group.copy()
        while dirty_group:
            sprite = dirty_group.sprites()[0]
            dirty_group.remove(sprite)
            for collided in pygame.sprite.spritecollide(sprite, all_group, False):
                if sprite is not collided:  # Do not include self
                    resolve_collision(sprite, collided)
                    dirty_group.add(sprite, collided)

        for sprite in all_group:
            # Apply wind resistance
            sprite.dx = sprite.dx * AIR_RESISTANCE
            sprite.dy = sprite.dy * AIR_RESISTANCE

            # Apply gravity
            sprite.dy += 10 - sprite.buoyancy

        dirty = all_group.draw(screen)
        pygame.display.update(dirty)

        # draw the scene
        clock.tick(40)


def resolve_wall_collision(sprite):
    inscreen = sprite.rect.clamp(SCREEN_RECT)
    if inscreen.centerx != sprite.rect.centerx:
        sprite.dx = -sprite.dx * sprite.bounce
    if inscreen.centery != sprite.rect.centery:
        sprite.dy = -sprite.dy * sprite.bounce
    sprite.rect = inscreen


def resolve_collision(sprite, collided):
    overlap = collided.rect.clip(sprite.rect)
    bounce = (sprite.bounce + collided.bounce) / 2
    if abs(sprite.dx - collided.dx) > abs(sprite.dy - collided.dy):
        # Horizontal collision
        mag = math.ceil(overlap.width / 2)
        screen_move(sprite.rect, mag if sprite.rect.centerx > collided.rect.centerx else -mag, 0)
        screen_move(collided.rect, -mag if sprite.rect.centerx > collided.rect.centerx else mag, 0)
        sprite.dx = -collided.dx * bounce
        collided.dx = -sprite.dx * bounce
    else:
        mag = math.ceil(overlap.height / 2)
        screen_move(sprite.rect, 0, mag if sprite.rect.centery > collided.rect.centery else -mag)
        screen_move(collided.rect, 0, -mag if sprite.rect.centery > collided.rect.centery else mag)
        sprite.dy = -collided.dy * bounce
        collided.dy = -sprite.dy * bounce


def screen_move(rect, x, y):
    rect.move_ip(x, y)
    rect.clamp_ip(SCREEN_RECT)


def has_quit():
    for event in pygame.event.get():
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            return True


if __name__ == '__main__':
    main()
