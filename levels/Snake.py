from setup import put
instructions = 'Make it to the door without being kiled by the Snakes!!'

next_level = 'guineapiggame'

door = put(600, 0, 'Door')
fudge = put(55, 0, 'Fudge Jumping')
put(400, 0, 'Snake')
put(320, 0, 'Snake')
put(160, 60, 'Snake')
put(360, 80, 'Snake')
put(145, 45, 'Snake')
put(250, 12, 'Snake')
put(200, 0, 'Snake')

def is_complete():
    global next_level

    if fudge.hit is door:
        return True

    #Game restart if fudge dies
    if fudge.hit is not None and fudge.hit.type_name == 'Snake':
        next_level = None
        return True
