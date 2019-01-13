Objects are things that can be added to a level. All objects appear as little images called _sprites_. Objects can be completely dumb and do nothing (like obstacles), or they can have behaviours (like characters), and even artificial intelligence if you're feeling ambitious!

# Creating a New Type of Object
First, add a small image file to the objects folder. This is the sprite image for the object, and it must exist.

## Object Images
The image file name must end in `.bmp`. You can make images like this with Paint. Here's the image for the character bob:

![bob](bob.bmp)

Generally, an image should have a black background, and be quite small. For example, bob is only 32 pixels wide and 32 pixels tall.

When the game detects if sprites are bumping into each other it uses the edges of the image canvas, not the edges of what you have drawn onto the canvas. So, take great care to draw all the way to the edge of the canvas (or make the canvas as small as possible around what you have drawn).

## Object Properties
An object can also have a Python script that tells the program about the object and how it should behave. This is a file with an extension of `.py`, also in the objects folder, with the same name as the object's image file.

You can add the following kinds of things to an object's script.
* `mass`: This is the mass of the object, as a decimal. If you don't include this, the value will be `10.0`.
* `elasticity`: This is the bounciness of the object when it collides with something, as a decimal between zero and one. If you don't include this, the value will be `0.3` (a bit bouncy).
* `buoyancy`: This is the floaty-ness of the object. Gravity pulls objects down, and this pulls objects up. A value of ten will make the object float in the middle of the screen. Less than that, it will sink under gravity; more, and it will float to the top of the screen. If you don't include this, the value will be `0.0` (not floaty at all).
* `portable`: This can be either `True` or `False`. By itself this property does nothing, but another object (say, a character), might check if an object is portable and allow the player to pick it up.
* `on_frame`: This is a function that defines how the object behaves all the time. We'll look more at this in the Behaviour section below.
* `action`: A function that defines some behaviour of the object _when another object, like a character, interacts with it_. We'll also see how this works below.

You can also add any other code you like to the script. This code will run right at the beginning of the game, before anything is shown on the screen.

Bear in mind that all these properties will apply to every copy of that object in a level. If you want different properties for some copies of your object, create a new copy of the object's image and script, with a new name (that is, just create a new object that looks the same).

## Object Behaviour
An object's behaviour is entirely defined inside a function called `on_frame`. This function is run 40 times a second, every time the screen is updated. It looks something like this:
```python
def on_frame(self, key_state):
  # Some code
```
There are two _arguments_ to the function, which must exist or the program will crash. These are `self` and `key_state`.

`self` represents the current copy of the object, which is being updated. Remember that there can be several copies of the same object in a level. Each copy (called an _instance_) has all the properties that we defined above, with the same values, but _also_ has some additional properties, which can be _different_ to any other copy, or instance. In `on_frame`, the values of these properties can be _changed_ - and this will not affect any other copy of the object, just this one. These are:
* `self.name`: the name of this copy. This starts out as the object name with a number added to it.
* `self.image`: the image of this copy. This is a pygame object called a [Surface](https://www.pygame.org/docs/ref/surface.html).
* `self.rect`: the location and size of this copy. This is a pygame object called a [Rect](https://www.pygame.org/docs/ref/rect.html).
* `self.hit`: if the copy is touching another object, then the value of this property will be whatever it is touching. Otherwise, it will be `None`.
* `self.speech`: if this copy is saying something, this will not be `None`.
* `self.carrying`: a list of other objects that this copy is carrying. You can add and remove from this list.

`key_state` contains any keys that are currently pressed by the player. This is a data structure called a _map_. To check whether a key is pressed, we have a look in the map using an expression like this:
```python
  if key_state[K_UP]:
    # Do something
```
The key names, like `K_UP` (for the up arrow key) are defined in the [pygame documentation](https://www.pygame.org/docs/ref/key.html). To use these names, you have to include the following at the top of your object script:
```python
from pygame.locals import *
```
