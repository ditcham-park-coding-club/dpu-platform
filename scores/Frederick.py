from beats import beat, repeat

def ney():
    beat()
    beat()
    beat(2)
    beat()
    beat()
    beat(2)
    beat()
    beat()
    beat(1.5)
    beat(0.5)
    beat()


ney()
repeat(ney, 3)
