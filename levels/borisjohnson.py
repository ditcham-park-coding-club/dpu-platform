from setup import put, all_group

instructions = "release all the balloons and release the several lonely peeople. Collect them."

next_level = 'yourmother'

level_complete = 'You released the five lonely people! High five! .... No? Suit yourself then'
put(0, 0, 'issybox')
put(0, 32, 'bob')
put(0, 32, 'box')
put(32, 32, 'box')
put(32, 96, 'box')

put(0, 64, 'issybox')
put(0, 100, 'box')
put(0, 132, 'box')
put(0, 164, 'box')
put(0, 196, 'box')
put(64, 32, 'box')
put(64, 64, 'issybox')

put(64, 132, 'box')
put(64, 0, 'box')
put(64, 100, 'box')
put(96, 132, 'box')

put(96, 100, 'box')
put(96, 132, 'box')
put(128, 0, 'box')
put(128, 363, 'box')
put(128, 272, 'issybox')
put(128, 32, 'box')
put(160, 0, 'box')
put(160, 373, 'box')
put(160, 352, 'box')
put(192, 123, 'box')

put(160, 64, 'issybox')
put(224, 123, 'box')
put(224, 236, 'box')

put(630, 0, 'wall')



def is_complete():
    for object in all_group:
        if object.type_name == 'box':
            return False
    return True
