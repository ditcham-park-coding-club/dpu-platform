import random
from setup import put, put_background

next_level = 'Guineapighutch'

objects = ['box', 'box', 'box', 'box', 'box', 'box', 'box', 'box', 'box', 'box', 'box',
 'box', 'box', 'box', 'box', 'box', 'box', 'box', 'box', 'box', 'box', 'box', 'box', 'box', 'Box Couch']
put(150, 150, 'Fudge Jumping')
put(0, 378, 'Pumpkin')
put(571, 354, 'marshmallow!!')
xcoordinate = [10, 30, 50, 70, 90, 110, 130, 150, 170, 190, 210, 230, 250, 270, 290, 310, 330, 350, 370, 390, 410, 430, 450, 470, 490, 510, 530, 550, 570, 590, 610]
ycoordinate = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 220, 240, 260, 280, 300, 320, 340, 360, 380, 400, 420, 440, 460]

box_couch = None

for object in objects:
    sprite = put(random.choice(xcoordinate), random.choice(ycoordinate), object)
    #print(sprite.name)
    if object == 'Box Couch':
        box_couch = sprite
        #print('found the box couch!')

def is_complete():
    if box_couch.count_down < 100:
        box_couch.count_down = box_couch.count_down - 1

    if box_couch.count_down == 0:
        return True
