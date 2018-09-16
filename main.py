import runpy
import sys
from beats import score, tick
from pygame import time

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        runpy.run_module("scores." + sys.argv[i])

    clock = time.Clock()

    while score:
        score.pop(0)()
        clock.tick(tick)
