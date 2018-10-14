from beats import beat, repeat, play

def bar():
    beat()
    beat(3)
    beat()

    beat()
    play('Crash-01')
    beat()
    beat(3)
    play('Crash-01')
    beat()

repeat(bar, 3)
