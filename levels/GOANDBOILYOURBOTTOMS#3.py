from setup import put

instructions = 'Get rid of the boxes to push Sexist Steve into the bin and release his prisoners!'

next_level = 'GOANDBOILYOURBOTTOMS#4'

put(0, 100, 'wall')
put(0, 300, 'wall')
sexiststeve = put(200,140, 'sexiststeve')
put(10, 448, 'bob')
put(630,0, 'wall')
put(630,100, 'wall')
put(200,480, 'box')
put(200,400, 'box')
put(200,320, 'issybox')
put(161,480, 'box')
put(161,400, 'box')
put(161,320, 'box')
put(161,240, 'box')
put(161,160, 'box')
put(161,80, 'box')
put(161,60, 'box')
put(161,40, 'box')
put(239,480, 'box')
put(239,440, 'box')
put(239,400, 'box')
put(239,360, 'box')
put(239,320, 'issybox')
put(239,280, 'box')
put(239,240, 'box')
put(239,200, 'box')
put(200,100, 'box')
put(200,60, 'box')
bin = put(500, 60, 'bin')

def is_complete():
    if sexiststeve.hit is bin:
        return True
