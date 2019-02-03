import runpy
import sys

from framestate import FrameState
from setup import *

MAX_ITERATIONS = 1000
WARN_ITERATIONS = 100

def main():
    # Run the requested start level
    level = run_level(sys.argv[1])
    clock = pygame.time.Clock()
    announce = None
    next_level_name = None

    while not has_quit():
        if not announce and level.get('is_complete') and level['is_complete']():
            all_group.empty()
            object_group.empty()
            next_level_name = level.get('next_level')
            complete_msg = level.get('level_complete') if 'level_complete' in level else 'Level Complete'
            announce = Text(complete_msg if next_level_name else 'Game Over')
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
    level = runpy.run_module("levels." + level_name, init_globals={
        k: previous_level[k] for k in previous_level
        if k not in ['is_complete', 'next_level', 'instructions']
    } if previous_level is not None else None)
    if level.get('instructions') is not None:
        instructions = Text(level['instructions'])
        instructions.y = 0
        instructions.rect.centerx = SCREEN_RECT.centerx
    return level


def has_quit():
    for event in pygame.event.get():
        if event.type == QUIT or \
                (event.type == KEYDOWN and event.key == K_ESCAPE):
            return True


if __name__ == '__main__':
    main()
