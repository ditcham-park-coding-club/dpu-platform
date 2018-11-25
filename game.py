import random
import runpy
import sys

from setup import *

AXES = [0, 1]


def next_axis(axis):
    return AXES[(axis + 1) % len(AXES)]


class FrameState(object):
    def __init__(self, sprite: Physical):
        self.sprite = sprite
        sprite.frame_state = self
        sprite.hit = None
        self._actual = (0, 0)
        self._target = tuple(map(int, (sprite.dx, sprite.dy)))
        self._next = (sprite.dx, sprite.dy)

    def try_move(self, finalise=False):
        progress = tuple(self._actual[axis] / self._target[axis] if self._target[axis] != 0 else 1.0 for axis in AXES)
        if any(p < 1.0 for p in progress):
            # Choose the axis with the furthest to go
            try_axis = progress.index(min(progress)) \
                if any(p != progress[0] for p in progress) else random.choice(AXES)
            if self._try_move(try_axis, finalise):
                return True
            else:
                # Try the other axis
                try_axis = next_axis(try_axis)
                if progress[try_axis] < 1.0:
                    return self._try_move(try_axis, finalise)

        return False

    def _try_move(self, try_axis, finalise):
        try_move = tuple((1 if self._target[axis] > 0 else -1) if try_axis == axis else 0 for axis in AXES)
        prev_rect = self.sprite.rect
        self.sprite.rect = prev_rect.move(*try_move)
        if self.sprite.rect.clamp(SCREEN_RECT).topleft != self.sprite.rect.topleft:
            if finalise:
                self.conserve_momentum(try_axis)
        else:
            collided = list(all_collisions(self.sprite))
            if not collided:
                # Moved! Increment actual progress.
                self._actual = tuple(self._actual[axis] + try_move[axis] for axis in AXES)
                return True
            elif finalise:
                for s2 in collided:
                    self.sprite.hit = s2  # Will select the last hit
                    self.conserve_momentum(try_axis, s2.frame_state)

        # Didn't move. Reset any putative movement.
        self.sprite.rect = prev_rect
        return False

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

    clock = pygame.time.Clock()

    while not has_quit():
        log(2, "---------------iteration----------------")
        all_group.clear(screen, background)
        all_group.update()

        # Apply keyboard state
        for s in object_group:
            s.on_frame(pygame.key.get_pressed())

        frame_states = list(map(FrameState, object_group))

        any_moved = True
        while any_moved:
            any_moved = False
            for fs in frame_states:
                any_moved = fs.try_move() or any_moved

        for fs in frame_states:
            fs.try_move(True)

        for fs in frame_states:
            fs.close()

        pygame.display.update(all_group.draw(screen))

        # draw the scene
        clock.tick(FRAME_RATE)


def has_quit():
    for event in pygame.event.get():
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            return True


if __name__ == '__main__':
    main()
