#i want it to move left right and jump
#i want it to say YES! when it collects somthing
#i want it to say GAME OVER when it dies
#i want it to behave differently
#i want heavy things to be static
#i want up arrow to be jukp and space to pick things up

from pygame.locals import K_RIGHT, K_LEFT, K_SPACE


def on_key(bob, key_state):
    if key_state[K_RIGHT]:
        bob.dx = 5
    elif key_state[K_LEFT]:
        bob.dx = -5

    if key_state[K_SPACE]:
        bob.dy = -30
