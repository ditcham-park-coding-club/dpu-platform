from setup import put, object_group, put_background

put_background(0, 0, 'objects/summernaturebackground.bmp')


instructions = "release all the balloons and release the several lonely peeople. Collect them."

next_level = 'guineapiggame'
#you have been working NON-STOP
#WE KNOW that your level is very good
#I like HURRICANEs
#know that you are my favourite person
#(is it true im your favwoute person?)
level_complete = 'You released the two lonely people! Now they can be lonely together'
put(0, 0, 'box')
put(0, 32, 'bob')
put(0, 32, 'box')
put(32, 32, 'box')
put(32, 96, 'box')

put(0, 64, 'box')
put(0, 100, 'box')
put(0, 132, 'box')
put(0, 164, 'box')
put(0, 196, 'box')
put(64, 32, 'box')
put(64, 64, 'issybox')

put(64, 132, 'box')
put(64, 0, 'box')

put(96, 132, 'box')

put(96, 100, 'box')
put(96, 132, 'box')
put(128, 0, 'box')
put(128, 363, 'box')

put(128, 32, 'box')
put(160, 0, 'box')
put(160, 373, 'box')

put(192, 123, 'box')

put(160, 64, 'issybox')
put(224, 123, 'box')


put(630, 0, 'bin')
put(400, 0, 'issybox')



def is_complete():
    for object in object_group:
        if object.type_name == 'box':
            return False
    return True
