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


def next_axis(axis):
    return AXES[(axis + 1) % len(AXES)]


class FrameState(object):
    def __init__(self, sprite: Physical):
        self.sprite = sprite
        self._actual = (0, 0)
        self._target = tuple(map(int, (sprite.dx, sprite.dy)))
        self._next = (sprite.dx, sprite.dy)

    def try_move(self, bounce=False):
        progress = self.get_progress()
        if any(p < 1.0 for p in progress):
            # Choose the axis with the furthest to go
            try_axis = progress.index(min(progress)) \
                if any(p != progress[0] for p in progress) else random.choice(AXES)
            if self._try_move(try_axis, bounce):
                return True
            else:
                # Try the other axis
                try_axis = next_axis(try_axis)
                if progress[try_axis] < 1.0:
                    return self._try_move(try_axis, bounce)

        return False

    def _try_move(self, try_axis, finalise):
        try_move = tuple((1 if self._target[axis] > 0 else -1) if try_axis == axis else 0 for axis in AXES)
        prev_rect = self.sprite.rect
        self.sprite.rect = prev_rect.move(*try_move)
        if self.sprite.rect.clamp(SCREEN_RECT).topleft != self.sprite.rect.topleft:
            if finalise:
                self.conserve_momentum(try_axis)
        else:
            collided = pygame.sprite.spritecollide(self.sprite, all_group, False)
            collided.remove(self.sprite)
            if not collided:
                # Moved! Increment actual progress.
                self._actual = tuple(self._actual[axis] + try_move[axis] for axis in AXES)
                return True
            elif finalise:
                for s2 in collided:
                    self.conserve_momentum(try_axis, s2.frame_state)

        # Didn't move. Reset any putative movement.
        self.sprite.rect = prev_rect
        return False

    def get_progress(self):
        return tuple(self._actual[axis] / self._target[axis] if self._target[axis] != 0 else 1.0 for axis in AXES)

    def conserve_momentum(self, axis, other=None, recurse=True):
        if other is None:  # Wall collision
            self.boink(axis, (-self.sprite.dx, -self.sprite.dy), self.sprite.elasticity, 1)
        else:
            self.boink(axis,
                       (other.sprite.dx - self.sprite.dx, other.sprite.dy - self.sprite.dy),
                       (self.sprite.elasticity + other.sprite.elasticity) / 2,
                       other.sprite.mass / (self.sprite.mass + other.sprite.mass))
            if recurse:
                other.conserve_momentum(axis, self, False)

    def boink(self, axis, delta, elasticity, momentum_share):
        self._next = tuple(delta[axis] * elasticity * momentum_share if a == axis else self._next[a] for a in AXES)

    def close(self):
        self.sprite.frame_state = None
        # Apply next delta and wind resistance
        (self.sprite.dx, self.sprite.dy) = map(lambda d: d * AIR_RESISTANCE, self._next)

        # Apply gravity
        self.sprite.dy += 10 - self.sprite.buoyancy


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
        while any_moved:
            any_moved = False
            for s in all_group:
                any_moved = s.frame_state.try_move() or any_moved

        for s in all_group:
            s.frame_state.try_move(True)

        for s in all_group:
            s.frame_state.close()

        dirty = all_group.draw(screen)
        pygame.display.update(dirty)

        # draw the scene
        clock.tick(40)


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
