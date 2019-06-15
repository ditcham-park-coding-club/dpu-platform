from setup import put, put_background

next_level = 'guineapiggame'

put_background(0, 0, 'objects/open hutch.bmp')

thething = put(0, 0, carrying[0].type_name)

def is_complete():
    if thething.moveable == False:
        return True
