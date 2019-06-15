import runpy
import sys

from framestate import FrameState
from setup import *

MAX_ITERATIONS = 1000
WARN_ITERATIONS = 100


class Level:
    farewell = 'Level Complete'
    next_level = None
    instructions = None

    @staticmethod
    def is_complete():
        return False


def main():
    # Run the requested start level
    level = run_level(sys.argv[1] if len(sys.argv) > 1 else 'example')
    clock = pygame.time.Clock()
    announce = None
    next_level_name = None

    while not has_quit():
        if not announce and level.is_complete():
            all_group.empty()
            object_group.empty()
            next_level_name = level.next_level
            announce = Text(level.farewell if next_level_name else 'Game Over')
            announce.rect.center = SCREEN_RECT.center

        if announce and not announce.alive():
            announce = None
            if next_level_name:
                level = run_level(next_level_name, level)
            else:
                return

        all_group.clear(screen, background)
        all_group.update()

        # Apply keyboard state
        for s in object_group:
            s.on_frame(pygame.key.get_pressed(), level)

        frame_states = list(map(FrameState, object_group))

        any_moved = True
        iterations = 0
        while any_moved and iterations < MAX_ITERATIONS:
            iterations = iterations + 1
            any_moved = False
            for fs in frame_states:
                any_moved = fs.try_move() or any_moved

        if iterations > WARN_ITERATIONS:
            log(1, f'Warning: Lots of iterations: {iterations}')

        for fs in frame_states:
            fs.try_move(True)

        for fs in frame_states:
            fs.close()

        # draw the scene
        pygame.display.update(all_group.draw(screen))

        clock.tick(FRAME_RATE)


def run_level(level_name, previous_level=None):
    level = type(level_name, (Level,), {
        # A Level is a singleton and never has any instance functions
        k: staticmethod(v) if callable(v) else v for k, v in
        runpy.run_module("levels." + level_name, init_globals=level_globals(previous_level)).items()
    })()
    if level.instructions is not None:
        instructions = Text(level.instructions)
        instructions.y = 0
        instructions.rect.centerx = SCREEN_RECT.centerx
    return level


def level_globals(previous_level):
    if previous_level is None:
        return {}
    else:
        base_level = Level()
        # Carry forward every level member except the base class ones
        return {
            k: getattr(previous_level, k)
            for k in dir(previous_level)
            if k not in dir(base_level)
        }


def has_quit():
    for event in pygame.event.get():
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            return True


if __name__ == '__main__':
    main()
