import random
import runpy
import sys

import pygame
from pygame.locals import *

from setup import all_group, screen, SCREEN_RECT, background, AIR_RESISTANCE, Physical

LOG_LEVEL = 1
AXES = [0, 1]


def log(level, string):
    if level <= LOG_LEVEL:
        print(string)


class FrameState(object):
    def __init__(self, sprite: Physical):
        self._sprite = sprite
        self._actual = (0, 0)
        self._target = tuple(map(int, (sprite.dx, sprite.dy)))
        self.can_move = (True, True)

    def try_move(self):
        progress = self.get_progress()
        # Claim 100% progress for any axis on which we can't move
        progress = tuple(progress[axis] if self.can_move[axis] else 1.0 for axis in AXES)
        if any(p < 1.0 for p in progress):
            # Choose the axis with the furthest to go
            try_axis = progress.index(min(progress)) \
                if any(p != progress[0] for p in progress) else random.choice(AXES)
            if self._try_move(try_axis):
                return True
            else:
                # Try the other axis
                try_axis = AXES[(try_axis + 1) % len(AXES)]
                if progress[try_axis] < 1.0:
                    return self._try_move(try_axis)

        return False

    def _try_move(self, try_axis):
        try_move = tuple((1 if self._target[axis] > 0 else -1) if try_axis == axis else 0 for axis in AXES)
        prev_rect = self._sprite.rect
        self._sprite.rect = prev_rect.move(*try_move)
        # If now touching the wall, set can_move to False for this axis
        if self._sprite.rect.clamp(SCREEN_RECT).topleft != self._sprite.rect.topleft:
            self.can_move = tuple(False if axis == try_axis else self.can_move[axis] for axis in AXES)
        else:
            collided = pygame.sprite.spritecollide(self._sprite, all_group, False)
            collided.remove(self._sprite)
            if not collided:
                # Moved! Increment actual progress.
                self._actual = tuple(self._actual[axis] + try_move[axis] for axis in AXES)
                return True
        # Didn't move. Reset any putative movement.
        self._sprite.rect = prev_rect
        return False

    def get_progress(self):
        return tuple(self._actual[axis] / self._target[axis] if self._target[axis] != 0 else 1.0 for axis in AXES)


def main():
    # Run the requested level
    runpy.run_module("levels." + sys.argv[1])

    # Report any initial collisions
    if not valid_level():
        return

    clock = pygame.time.Clock()

    while not has_quit():
        log(2, "---------------iteration----------------")
        all_group.clear(screen, background)

        # Apply keyboard state
        for s in all_group:
            s.on_key(pygame.key.get_pressed())
            s.hit = None
            s.frame_state = FrameState(s)

        any_moved = True
        movable_group = all_group.copy()
        while any_moved and movable_group:
            any_moved = False
            for s in movable_group:
                any_moved = s.frame_state.try_move() or any_moved
                if not any(s.frame_state.can_move):
                    movable_group.remove(s)

        # TODO Conserve momentum for any final collisions
        for s in all_group:
            if any(p < 1.0 for p in s.frame_state.get_progress()):
                (s.dx, s.dy) = (0.0, 0.0)

        for s in all_group:
            # Apply wind resistance
            (s.dx, s.dy) = (s.dx * AIR_RESISTANCE, s.dy * AIR_RESISTANCE)

            # Apply gravity
            s.dy += 10 - s.buoyancy

        dirty = all_group.draw(screen)
        pygame.display.update(dirty)

        # draw the scene
        clock.tick(40)


def conserve_momentum(s, s2=None, recurse=True):
    if s2 is None:  # Wall collision
        # boink(s, -s.dx, -s.dy, s.elasticity, 1)
        s.next = (0, 0)
    else:
        boink(s, s.dx - s2.dx, s.dy - s2.dy,
              (s.elasticity + s2.elasticity) / 2,
              s2.mass / (s.mass + s2.mass))
        if recurse:
            conserve_momentum(s2, s, False)


def boink(s, dx, dy, elasticity, momentum_share):
    if s.target[0] != 0:
        s.next[0] = dx * elasticity * momentum_share
    if s.target[1] != 0:
        s.next[1] = dy * elasticity * momentum_share


def valid_level():
    okay = True
    for s in all_group:
        if not SCREEN_RECT.contains(s.rect):
            clamped = s.rect.clamp(SCREEN_RECT)
            log(1, f"{s.name} is not on the screen, try {clamped.x, clamped.y}")
            okay = False
        collisions = pygame.sprite.spritecollide(s, all_group, False)
        collisions.remove(s)
        for c in collisions:
            okay = False
            log(1, f"{s.name} is overlapping with {c.name}")
    return okay


def has_quit():
    for event in pygame.event.get():
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            return True


if __name__ == '__main__':
    main()
