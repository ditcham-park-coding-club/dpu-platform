from pygame import mixer
from math import floor

# Smaller than default buffer size increases timing accuracy
mixer.init(buffer = 1024)

bpm = 120 # 2 beats per second

tick = 32 # 32 ticks per second

tick_duration = 1 / tick
beat_duration = 60 / bpm
ticks_per_beat = beat_duration / tick_duration

score = []

sounds = {'snare': mixer.Sound('snare.ogg')}

def beat(beats = 1):
    play('snare', beats)

def play(sound, beats):
    score.append(lambda: sounds[sound].play())
    score.extend([lambda: None] * (floor(ticks_per_beat * beats) - 1))
