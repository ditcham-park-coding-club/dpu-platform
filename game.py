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

        # Apply keyboard state
        for sprite in all_group:
            sprite.on_key(sprite, pygame.key.get_pressed())

        # Apply velocity
        for sprite in all_group:
            sprite.next_dx = sprite.dx
            sprite.next_dy = sprite.dy
            screen_move(sprite, sprite.dx, sprite.dy)

        # Resolve collisions with walls and other sprites
        dirty_group = all_group.copy()
        while dirty_group:
            sprite = dirty_group.sprites()[0]
            dirty_group.remove(sprite)
            collided = pygame.sprite.spritecollideany(sprite, dirty_group)
            if collided is not None:
                resolve_collision(sprite, collided)
                dirty_group.add(sprite, collided)

        for sprite in all_group:
            # Apply wind resistance
            sprite.dx = sprite.next_dx * AIR_RESISTANCE
            sprite.dy = sprite.next_dy * AIR_RESISTANCE

            # Apply gravity
            sprite.dy += 10 - sprite.buoyancy

        dirty = all_group.draw(screen)
        pygame.display.update(dirty)

        # draw the scene
        clock.tick(40)


def screen_move(sprite, x, y, next_dx=None, next_dy=None):
    start = sprite.rect
    moved = start.move(x, y)
    sprite.rect = moved.clamp(SCREEN_RECT)

    if sprite.rect.centerx != moved.centerx:
        sprite.next_dx = 0.0
    elif next_dx is not None:
        sprite.next_dx = next_dx

    if sprite.rect.centery != moved.centery:
        sprite.next_dy = 0.0
    elif next_dy is not None:
        sprite.next_dy = next_dy

    return sprite.rect.centerx - start.centerx, sprite.rect.centery - start.centery


def resolve_collision(s1, s2):
    overlap = s2.rect.clip(s1.rect)
    total_mass = s2.mass + s1.mass
    x_speed = abs(s1.dx - s2.dx)
    y_speed = abs(s1.dy - s2.dy)
    horizontal_collision = x_speed > y_speed \
        if not math.isclose(x_speed, y_speed) \
        else overlap.height > overlap.width

    if horizontal_collision:
        correct = math.ceil(overlap.width / 2)
        direction = 1 if overlap.right == s1.rect.right else -1
        next_dx = (s1.mass * s1.dx + s2.mass * s2.dx) / total_mass
        (actual, _) = screen_move(s1, -correct * direction, 0, next_dx)
        screen_move(s2, (correct - actual) * direction, 0, next_dx)
    else:
        correct = math.ceil(overlap.height / 2)
        direction = 1 if overlap.bottom == s1.rect.bottom else -1
        next_dy = (s1.mass * s1.dy + s2.mass * s2.dy) / total_mass
        (_, actual) = screen_move(s1, 0, -correct * direction, None, next_dy)
        screen_move(s2, 0, (correct - actual) * direction, None, next_dy)


def has_quit():
    for event in pygame.event.get():
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            return True


if __name__ == '__main__':
    main()
