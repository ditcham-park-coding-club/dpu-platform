#._.._..._.:..:...

from beats import beat, repeat, play

def bar():
    beat(2)
    beat(1)
    beat(1)
    beat(1)
    beat(1)
    beat(1)
    beat(1)
    beat(0.5)
    beat(0.5)
    beat(1)
    beat(0.5)
    beat(0.5)
    beat(1)
    beat(1)
    play('Crash-02')

    def bars():
        play('kick-02', 0.5)
        play('kick-02')
        play('kick-02', 2)

repeat(bar, 3)
repeat(bars, 3)
