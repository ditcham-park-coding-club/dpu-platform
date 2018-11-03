from beats import beat, play, repeat, together
def fud():
    play('Kick-02', 1)

def naa():
    play('OpHat-01', 1)

def anotherElderberry():
    beat(0.5)
    beat(1.5)

def ell():
    beat(1.5)
    beat(0.25)
    beat(0.25)


def haha():
    anotherElderberry()
    anotherElderberry()
    ell()
    anotherElderberry()

def ooh():
    naa()
    fud()
    naa()
    fud()

def ka():
    together(fud, beat)

repeat(haha, 2)
repeat(ooh, 2)
haha()
ka()
