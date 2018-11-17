from pygame.locals import K_RIGHT, K_LEFT, K_SPACE


def on_key(bob, key_state):
    if key_state[K_RIGHT]:
        bob.dx = 5
    elif key_state[K_LEFT]:
        bob.dx = -5

    if key_state[K_SPACE]:
        bob.dy = -30
