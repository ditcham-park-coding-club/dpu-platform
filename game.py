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
            sprite.rect.move_ip(sprite.dx, sprite.dy)
            sprite.next_dx = sprite.dx
            sprite.next_dy = sprite.dy
            resolve_wall_collision(sprite)

        # Resolve collisions with walls and other sprites
        dirty_group = all_group.copy()
        while dirty_group:
            sprite = dirty_group.sprites()[0]
            dirty_group.remove(sprite)
            collided = pygame.sprite.spritecollideany(sprite, dirty_group)
            if collided is not None:
                resolve_collision(sprite, collided)
                resolve_wall_collision(sprite, collided)
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


def resolve_wall_collision(*sprites):
    for sprite in sprites:
        in_screen = sprite.rect.clamp(SCREEN_RECT)
        if sprite.rect.center != in_screen.center:
            if in_screen.centerx != sprite.rect.centerx:
                sprite.next_dx = -sprite.dx * sprite.bounce
                sprite.dx = 0.0  # Instantaneously stopped
            if in_screen.centery != sprite.rect.centery:
                sprite.next_dy = -sprite.dy * sprite.bounce
                sprite.dy = 0.0  # Instantaneously stopped
            sprite.rect = in_screen


def resolve_collision(s1, s2):
    overlap = s2.rect.clip(s1.rect)
    bounce = (s1.bounce + s2.bounce) / 2
    total_mass = s2.mass + s1.mass
    x_speed = abs(s1.dx - s2.dx)
    y_speed = abs(s1.dy - s2.dy)
    horizontal_collision = x_speed > y_speed \
        if not math.isclose(x_speed, y_speed) \
        else overlap.height > overlap.width

    if horizontal_collision:
        # Horizontal collision
        correct = math.ceil(overlap.width / 2)
        s1.rect.move_ip(correct if s1.rect.centerx > s2.rect.centerx else -correct, 0)
        s2.rect.move_ip(-correct if s1.rect.centerx > s2.rect.centerx else correct, 0)
        s1.next_dx = (s2.dx - s1.dx) * (s2.mass / total_mass) * bounce
        s2.next_dx = (s1.dx - s2.dx) * (s1.mass / total_mass) * bounce
    else:
        correct = math.ceil(overlap.height / 2)
        s1.rect.move_ip(0, correct if s1.rect.centery > s2.rect.centery else -correct)
        s2.rect.move_ip(0, -correct if s1.rect.centery > s2.rect.centery else correct)
        s1.next_dy = (s2.dy - s1.dy) * (s2.mass / total_mass) * bounce
        s2.next_dy = (s1.dy - s2.dy) * (s1.mass / total_mass) * bounce

    # Instantaneously sticky
    s1.dx = s2.dx = (s1.mass * s1.dx + s2.mass * s2.dx) / total_mass
    s1.dy = s2.dy = (s1.mass * s1.dy + s2.mass * s2.dy) / total_mass


def screen_move(rect, x, y):
    moved = rect.move(x, y).clamp(SCREEN_RECT)
    rect.center = moved.center
    return moved.centerx - rect.centerx, moved.centery - rect.centery


def has_quit():
    for event in pygame.event.get():
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            return True


if __name__ == '__main__':
    main()
