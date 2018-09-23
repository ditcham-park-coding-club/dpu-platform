from pygame import mixer
from math import floor
from os import listdir

# Smaller than default buffer size increases timing accuracy
mixer.init(buffer = 1024)

bpm = 120 # 2 beats per second

tick = 32 # 32 ticks per second

tick_duration = 1 / tick
beat_duration = 60 / bpm
ticks_per_beat = beat_duration / tick_duration

score = []
position = 0

drums = {fn.rsplit('.', 1)[0]: mixer.Sound('kit/' + fn) for fn in listdir('kit')}

def beat(beats = 1):
    play('Snr-01', beats)

def play(drum, beats = 1):
    _score(lambda: drums[drum].play())
    _score(lambda: None, floor(ticks_per_beat * beats) - 1)

def together(*parts):
    global position
    startPos = position
    for part in parts:
        position = startPos
        part()

def _score(action, repeat = 1):
    global position
    if position == len(score):
        score.extend([action] * repeat)
        position += repeat
    elif repeat == 1:
        also = score[position]
        score[position] = lambda: _together(action, also)
        position += 1
    else:
        _score(action, 1)
        _score(action, repeat - 1)

def _together(*fns):
    for fn in fns:
        fn()
