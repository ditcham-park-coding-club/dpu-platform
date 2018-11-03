from beats import beat, repeat, play, together

def funk():
    beat(0.5)
    beat()
    beat(0.5)
    beat()
    beat()

def kick():
    play('Kick-01')

def bass():
    repeat(kick, 4)

together(bass, funk)
