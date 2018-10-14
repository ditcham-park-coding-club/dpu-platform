from beats import beat, repeat, play, together, rest

def kick():
    play('Kick-01', 1)

def bass():
    repeat(kick, 4)

def funk():
    beat(0.5)
    beat()
    beat(0.5)
    beat()
    beat()

repeat(funk, 3)
