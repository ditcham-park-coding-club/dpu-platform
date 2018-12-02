from pygame.locals import K_RIGHT, K_LEFT, K_SPACE, K_UP, K_DOWN


def on_key(bob, key_state):
    if key_state[K_RIGHT]:
        bob.dx = 10
    elif key_state[K_LEFT]:
        bob.dx = -10

    if key_state[K_UP]:
        bob.dy = -10

    if key_state[K_DOWN]:
        bob.dy = 10
