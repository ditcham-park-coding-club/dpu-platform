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

            # Detect and resolve collisions with the walls
            inscreen = sprite.rect.clamp(SCREEN_RECT)
            if inscreen.centerx != sprite.rect.centerx:
                sprite.dx = -sprite.dx * sprite.bounce
            if inscreen.centery != sprite.rect.centery:
                sprite.dy = -sprite.dy * sprite.bounce
            sprite.rect = inscreen

            # Resolve collisions
            for collided in pygame.sprite.spritecollide(sprite, all_group, False):
                if sprite is not collided:
                    overlap = collided.rect.clip(sprite.rect)
                    bounce = (sprite.bounce + collided.bounce) / 2
                    if abs(sprite.dx - collided.dx) > abs(sprite.dy - collided.dy):
                        # Horizontal collision
                        mag = overlap.width / 2
                        sprite.rect.move_ip(mag if sprite.rect.centerx > collided.rect.centerx else -mag, 0)
                        collided.rect.move_ip(-mag if sprite.rect.centerx > collided.rect.centerx else mag, 0)
                        sprite.dx = -collided.dx * bounce
                        collided.dx = -sprite.dx * bounce
                    else:
                        mag = overlap.height / 2
                        sprite.rect.move_ip(0, mag if sprite.rect.centery > collided.rect.centery else -mag)
                        collided.rect.move_ip(0, -mag if sprite.rect.centery > collided.rect.centery else mag)
                        sprite.dy = -collided.dy * bounce
                        collided.dy = -sprite.dy * bounce

            # Apply wind resistance
            sprite.dx = sprite.dx * AIR_RESISTANCE
            sprite.dy = sprite.dy * AIR_RESISTANCE

            # Apply gravity
            sprite.dy += 5

        dirty = all_group.draw(screen)
        pygame.display.update(dirty)

        # draw the scene
        clock.tick(40)


def has_quit():
    for event in pygame.event.get():
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            return True


if __name__ == '__main__':
    main()
