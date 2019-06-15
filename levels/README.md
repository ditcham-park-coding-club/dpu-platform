# Creating a Level

First, add a level to the levels folder. The level file name must end in `.py`.

A level is a Python script that tells the program what the level should contain and what should happen in it.

The simplest thing you can do is add an object to the level, using the function `put()` (which is available in the `setup` package). The `put` function takes three _arguments_ (also called _parameters_):
1. The object name, as a string (in quotes), selected from the file names ending in `.bmp` in the [objects](/objects) folder. For example, `'box'`.
1. The horizontal position to put the object (its `x` coordinate), from the left. The screen has a total of 640 pixels across.
1. The vertical position to put the object (its `y` coordinate), from the top (yes, down. In programming, the `y` axis is almost always down from the top of the screen). The screen has a total of 480 pixels down.

So, the simplest possible level looks something like this:
```python
from setup import put

put('box', 100, 100)
```
If you create a level like this, you'll see that the box appears towards the top-left of the screen, then immediately drops, under gravity, to the bottom.

If you try to put an object outside of the screen, or overlapping another object, the program will try its best to shuffle it somewhere more sensible. So it might not appear exactly where you tried to put it. When this happens, a warning will be written out to the console.

Different objects might have different properties and behaviours. See the [objects README](/objects/README.md) for more about objects.

When you `put` an object, the function returns a reference to the object which you can use later, for example, in `is_complete` (see below).

You can also define the following kinds of things in a level. See the [example level](/levels/example.py) for examples of these.

* `instructions`: if there is a string variable with this name, then the value will be shown for a moment when the level starts.
* `farewell`: if there is a string variable with this name, then the value will be shown for a moment when the level has completed.
* `next_level`: if there is a string variable with this name, then when the level is complete (see below), the game will move to the level named as the variable's value.
* `is_complete`: if there is a function with this name, the function will be called whenever anything happens in the level. If the function, when called, returns `True`, then the level will be over and the game will move to the next level.
