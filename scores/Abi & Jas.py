from beats import beat, repeat, play, together

def bar():
    beat(2)
    beat(1)
    beat(2)
    beat(1)
    beat(1)
    beat(1)
    beat(0.5)
    beat(0.5)
    beat(1)
    beat(0.5)
    beat(0.5)
    beat(1)
    play('Crash-02')

def bass():
    play('Tom-05', 2)
    play('Tom-05', 0.5)
    play('Tom-05', 0.5)
    play('Tom-05')
    play('Tom-05', 2)
    play('Tom-05', 0.5)
    play('Tom-05', 0.5)
    play('Tom-05')
    play('Tom-05', 2)
    play('Tom-05', 0.5)
    play('Tom-05', 0.5)
    play('Tom-05')

def ting():
    play('Kick-02', 0.5)
    play('Kick-02', 0.5)
    play('Kick-02')
    play('Kick-02')
    play('Kick-02', 0.5)
    play('Kick-02', 0.5)
    play('Kick-02')
    play('Kick-02')
    play('Kick-02', 0.5)
    play('Kick-02', 0.5)
    play('Kick-02', 2)
    play('Crash-02')

repeat(bass, 1)

together(bar, bass)

together(bar, bass, ting)

repeat(ting, 1)
