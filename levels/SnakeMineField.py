from setup import put
instructions = 'Make it to the door without being kiled by the Snakes!!'

level_complete = 'Congratulations on not dying!'

next_level = 'guineapiggame'

door = put(600, 0, 'Door')
fudge = put(55, 0, 'Fudge Jumping')
put(430, 0, 'Snake')
put(490, 0, 'Snake')
snake3 = put(160, 60, 'Snake')
snake3.buoyancy = 10

put(360, 0, 'Snake')
put(290, 45, 'Snake')
snakebob = put(333, 12, 'Snake')
snakebob.buoyancy=10
put(280, 0, 'Snake')

def is_complete():
    global next_level

    if fudge.hit is door:
        return True

    if fudge.hit is not None and fudge.hit.type_name == 'Snake':
        next_level = None
        return True
