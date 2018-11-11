import runpy
import sys

import pygame
from pygame.locals import *

from setup import all_group, screen, SCREEN_RECT, background, AIR_RESISTANCE


def main():
    # Run the requested level
    runpy.run_module("levels." + sys.argv[1])

    clock = pygame.time.Clock()

    while not has_quit():
        all_group.clear(screen, background)

        for sprite in all_group:
            # Apply velocity
            sprite.rect.move_ip(sprite.dx, sprite.dy)

        for sprite in all_group:
            # Resolve collisions with the walls - always wins
            if resolve_wall_collision(sprite):
                # Resolve collisions with other sprites
                for collided in pygame.sprite.spritecollide(sprite, all_group, False):
                    resolve_collision(sprite, collided)

            # Apply wind resistance
            sprite.dx = sprite.dx * AIR_RESISTANCE
            sprite.dy = sprite.dy * AIR_RESISTANCE

            # Apply gravity
            sprite.dy += 5

        dirty = all_group.draw(screen)
        pygame.display.update(dirty)

        # draw the scene
        clock.tick(40)


def resolve_wall_collision(sprite):
    inscreen = sprite.rect.clamp(SCREEN_RECT)
    if inscreen.center != sprite.rect.center:
        if inscreen.centerx != sprite.rect.centerx:
            sprite.dx = -sprite.dx * sprite.bounce
        if inscreen.centery != sprite.rect.centery:
            sprite.dy = -sprite.dy * sprite.bounce
        sprite.rect = inscreen
        return False
    return True


def resolve_collision(sprite, collided):
    if sprite is not collided:  # Do not include self
        overlap = collided.rect.clip(sprite.rect)
        bounce = (sprite.bounce + collided.bounce) / 2
        if abs(sprite.dx - collided.dx) > abs(sprite.dy - collided.dy):
            # Horizontal collision
            mag = overlap.width / 2
            screen_move(sprite.rect, mag if sprite.rect.centerx > collided.rect.centerx else -mag, 0)
            screen_move(collided.rect, -mag if sprite.rect.centerx > collided.rect.centerx else mag, 0)
            sprite.dx = -collided.dx * bounce
            collided.dx = -sprite.dx * bounce
        else:
            mag = overlap.height / 2
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
