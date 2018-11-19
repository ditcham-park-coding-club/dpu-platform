import runpy
import sys

import pygame
from pygame.locals import *

from setup import all_group, screen, SCREEN_RECT, background, AIR_RESISTANCE

LOG_LEVEL = 1


def log(level, string):
    if level <= LOG_LEVEL:
        print(string)


def decrement_of(d):
    return -1 if d > 0 else 1 if d < 0 else 0


def main():
    # Run the requested level
    runpy.run_module("levels." + sys.argv[1])

    # Report any initial collisions
    any_bad = False
    for s in all_group:
        if not SCREEN_RECT.contains(s.rect):
            clamped = s.rect.clamp(SCREEN_RECT)
            log(1, f"{s.name} is not on the screen, try {clamped.x, clamped.y}")
            any_bad = True
        collisions = pygame.sprite.spritecollide(s, all_group, False)
        collisions.remove(s)
        for c in collisions:
            any_bad = True
            log(1, f"{s.name} is overlapping with {c.name}")

    if any_bad:
        return

    clock = pygame.time.Clock()

    while not has_quit():
        log(2, "---------------iteration----------------")
        all_group.clear(screen, background)

        # Apply keyboard state
        for s in all_group:
            s.on_key(pygame.key.get_pressed())
            s.hit = None
            s.next_dx = s.dx
            s.next_dy = s.dy
            s.prev_rect = s.rect
            (s.int_dx, s.int_dy) = map(int, (s.dx, s.dy))

        changed = True
        while changed:
            changed = False
            for s in all_group:
                s.rect = s.prev_rect.move(s.int_dx, s.int_dy)

            for s in all_group:
                # Wall collision
                if not SCREEN_RECT.contains(s.rect):
                    clamped = s.rect.clamp(SCREEN_RECT)
                    s.int_dx = clamped.x - s.prev_rect.x
                    s.int_dy = clamped.y - s.prev_rect.y
                    conserve_momentum(s)
                    log(2, f"{s.name} collided wall")
                    changed = True
                else:
                    # Other sprite collision
                    collisions = pygame.sprite.spritecollide(s, all_group, False)
                    collisions.remove(s)
                    if collisions:
                        changed = True
                        for c in collisions:
                            # Would the axes in isolation have caused a collision?
                            blame_x = c.prev_rect.move(c.int_dx, 0).colliderect(s.rect)
                            blame_y = c.prev_rect.move(0, c.int_dy).colliderect(s.rect)
                            # If we can't decide, move both
                            if blame_x or (not blame_x and not blame_y):
                                c.int_dx += decrement_of(c.int_dx)
                            if blame_y or (not blame_x and not blame_y):
                                c.int_dy += decrement_of(c.int_dy)
                            log(2, f"{s.name} collided {c.name} having speed ({c.int_dx}, {c.int_dy})")
                            s.hit = c
                            conserve_momentum(s, c)

        for s in all_group:
            # Apply wind resistance
            s.dx = s.next_dx * AIR_RESISTANCE
            s.dy = s.next_dy * AIR_RESISTANCE

            # Apply gravity
            s.dy += 10 - s.buoyancy

        dirty = all_group.draw(screen)
        pygame.display.update(dirty)

        # draw the scene
        clock.tick(40)


def conserve_momentum(s, s2=None, recurse=True):
    if s2 is None:  # Wall collision
        # boink(s, -s.dx, -s.dy, s.elasticity, 1)
        s.next_dx = s.next_dy = 0
    else:
        boink(s, s.dx - s2.dx, s.dy - s2.dy,
              (s.elasticity + s2.elasticity) / 2,
              s2.mass / (s.mass + s2.mass))
        if recurse:
            conserve_momentum(s2, s, False)


def boink(s, dx, dy, elasticity, momentum_share):
    if s.int_dx != 0:
        s.next_dx = dx * elasticity * momentum_share
    if s.int_dy != 0:
        s.next_dy = dy * elasticity * momentum_share


def has_quit():
    for event in pygame.event.get():
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            return True


if __name__ == '__main__':
    main()
