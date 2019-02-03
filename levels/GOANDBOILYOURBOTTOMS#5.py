from setup import put

instructions = 'Get rid of the boxes to push Dodgy Dan into the bin!'

level_complete = 'Congrats! you have rid a small, virtual, non-existent world of \n a little bit of non-existent evil. you cant do everything.'

next_level = 'borisjohnson'

put(0, 100, 'wall')
put(0, 300, 'wall')
dodgydan = put(200,140, 'dodgydan')
put(10, 448, 'bob')
put(630,0, 'wall')
put(630,100, 'wall')
put(200,480, 'box')
put(200,400, 'box')
put(200,320, 'box')
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
put(239,320, 'box')
put(239,280, 'box')
put(239,240, 'box')
put(239,200, 'box')
put(200,100, 'box')
put(200,60, 'box')
bin = put(500, 60, 'bin')

def is_complete():
    if dodgydan.hit is bin:
        return True
