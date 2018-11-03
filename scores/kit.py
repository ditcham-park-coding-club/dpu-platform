from beats import beat, repeat, play, together

def bar():
    beat()
    beat(3)
    beat()

def hi():
    beat()
    play('Crash-01')
    beat()
    beat(3)
    play('Crash-01')
    beat()

repeat(bar, 3)
together(bar, hi)
