from pygame import mixer
from math import floor

mixer.init()

beat = 0.5 # 2 beats per second

tick = 0.03125 # 32 ticks per second

music = []

sounds = {'snare': mixer.Sound('snare.ogg')}

def snare(duration):
    play('snare', duration)

def play(sound, duration):
    music.append(lambda: sounds[sound].play())
    music.extend([lambda: None] * (floor((duration * beat) / tick) - 1))
