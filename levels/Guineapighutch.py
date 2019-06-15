from setup import put, put_background

next_level = 'guineapiggame'

put_background(0, 0, 'objects/open hutch.bmp')

thething = put(0, 0, last_found_furniture_type)

# Have we been to this level before? (Is there a furniture variable?)
if 'furniture' in globals():
    # Replace the furniture that we placed last time
    for type_name, (x, y) in furniture.items():
        put(x, y, type_name).moveable = False
else:
    # Create the furniture variable as an empty Python dict
    furniture = {}

def is_complete():
    if thething.moveable == False:
        # Record exactly where the new furniture was placed
        furniture[last_found_furniture_type] = (thething.rect.x, thething.rect.y)
        return True
