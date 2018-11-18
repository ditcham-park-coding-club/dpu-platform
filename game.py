import runpy
import sys
import random

import pygame
from pygame.locals import *

from setup import all_group, screen, SCREEN_RECT, background, AIR_RESISTANCE


def log(string):
    if True:
        print(string)


def reverse(d, hint_d=0):
    return 1 if d < 0 else -1 if d > 0 else reverse(hint_d) if hint_d != 0 else random.choice([1, -1])


def back_off(s, dx, dy, hint_dx, hint_dy):
    (dx, dy, hint_dx, hint_dy) = map(int, (dx, dy, hint_dx, hint_dy))
    do_x = do_y = True
    if abs(dx) != abs(dy):
        do_x = abs(dx) > abs(dy)
        do_y = abs(dy) > abs(dx)
    elif abs(hint_dx) != abs(hint_dy):
        do_x = abs(hint_dx) > abs(hint_dy)
        do_y = abs(hint_dy) > abs(hint_dx)

    rx = reverse(dx, hint_dx) if do_x else 0
    ry = reverse(dy, hint_dy) if do_y else 0

    log(f"{s.name} at:({s.rect.x}, {s.rect.y}) "
        f"speed:({dx}, {dy}) "
        f"hint:({hint_dx}, {hint_dy}) "
        f"will back off:({rx}, {ry})")
    s.rect.move_ip(rx, ry)
    s.backoff_count = s.backoff_count + 1

    return do_x, do_y


def clip_dir_x(rect, clip):
    return -1 if clip.left > rect.left else 1 if clip.right < rect.right else 0


def clip_dir_y(rect, clip):
    return -1 if clip.top > rect.top else 1 if clip.bottom < rect.bottom else 0


def main():
    # Run the requested level
    runpy.run_module("levels." + sys.argv[1])

    clock = pygame.time.Clock()

    while not has_quit():
        log("---------------iteration----------------")
        all_group.clear(screen, background)

        # Apply keyboard state
        for s in all_group:
            s.on_key(s, pygame.key.get_pressed())

        # Apply velocity
        for s in all_group:
            s.next_dx = s.dx
            s.next_dy = s.dy
            s.backoff_count = 0
            s.rect.move_ip(s.dx, s.dy)  # involves integer truncation

        # Resolve collisions with walls and other sprites.
        dirty_group = all_group.copy()
        while dirty_group:
            s = random.choice(dirty_group.sprites())  # dirty_group.sprites()[0]
            dirty_group.remove(s)

            clamped = s.rect.clamp(SCREEN_RECT)
            if clamped.center != s.rect.center:
                # Wall collision
                log(f"{s.name} collided wall")
                clip = SCREEN_RECT.clip(s.rect)
                axes = back_off(s,
                                clip_dir_x(s.rect, clip) * (s.rect.width - clip.width),
                                clip_dir_y(s.rect, clip) * (s.rect.height - clip.height),
                                s.dx, s.dy)
                dirty_group.add(s)
                conserve_momentum(*axes, s)

            # Other sprite collision
            collided = pygame.sprite.spritecollide(s, all_group, False)
            collided.remove(s)
            if collided:
                s2 = random.choice(collided)
                log(f"{s.name} collided {s2.name}")
                clip = s.rect.clip(s2.rect)
                to_back_off = s if s.backoff_count < s2.backoff_count else \
                    s2 if s2.backoff_count < s.backoff_count else random.choice([s, s2])
                other = s2 if to_back_off is s else s
                axes = back_off(to_back_off,
                                to_back_off.dx - other.dx,
                                to_back_off.dy - other.dy,
                                -clip_dir_x(to_back_off.rect, clip) * (s.rect.width - clip.width),
                                -clip_dir_y(to_back_off.rect, clip) * (s.rect.height - clip.height))
                dirty_group.add(s, s2)
                conserve_momentum(*axes, s, s2)

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


def conserve_momentum(do_x, do_y, s, s2=None, recurse=True):
    if s2 is None:  # Wall collision
        boink(s, do_x, do_y, -s.dx, -s.dy, s.elasticity, 1)
    else:
        boink(s, do_x, do_y, s.dx - s2.dx, s.dy - s2.dy,
              (s.elasticity + s2.elasticity) / 2,
              s2.mass / (s.mass + s2.mass))
        if recurse:
            conserve_momentum(do_x, do_y, s2, s, False)


def boink(s, do_x, do_y, dx, dy, elasticity, momentum_share):
    if do_x:
        s.next_dx = dx * elasticity * momentum_share
    if do_y:
        s.next_dy = dy * elasticity * momentum_share


def has_quit():
    for event in pygame.event.get():
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            return True


if __name__ == '__main__':
    main()
