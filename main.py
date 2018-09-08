import runpy
import sys
from beats import music, tick, beat
from pygame import time, mixer
from math import floor

if __name__ == '__main__':
    for i in range(1, len(sys.argv)):
        runpy.run_module(sys.argv[i])

    clock = time.Clock()

    while music:
        music.pop(0)()
        clock.tick(tick * 1000)
