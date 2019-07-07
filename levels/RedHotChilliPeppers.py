from setup import put
instructions = 'Make it to the door without being kiled by the Red Hot Chilli Peppers!!'

farewell = 'Congratulations on not dying!'

next_level = 'borisjohnson'

door = put(600, 0, 'Door')
fudge = put(55, 0, 'Fudge Jumping')
snake1 = put(430, 0, 'Snake')
snake1.going_left = False
put(490, 0, 'Snake')
snake3 = put(160, 60, 'Snake')
snake3.buoyancy = 10
snake3.mass = 1000
snake3.going_left = False

snake4 = put(360, 0, 'Snake')
snake4.buoyancy = 10

put(290, 45, 'Snake')
snakebob = put(333, 12, 'Snake')
snakebob.buoyancy=10
snakebob.going_left = False
put(280, 0, 'Snake')

def is_complete():
    if fudge.hit is door:
        return True

    if fudge.hit is not None and fudge.hit.type_name == 'Snake':
        next_level = None
        return True
