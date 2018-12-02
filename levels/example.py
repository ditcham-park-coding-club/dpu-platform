from setup import put

instructions = 'Collect two balloons to complete the level'

next_level = 'GOANDBOILYOURBOTTOMS'

boris = put(64, 80, 'boris')

put(0, 300, 'wall')
put(100, 32, 'balloon')
put(32, 80, 'box')
put(342, 80, 'box')
put(23, 112, 'box')
put(22, 144, 'box')
put(265, 80, 'box')
put(300, 80, 'box')


def is_complete():
    balloon_count = 0
    for obj in boris.carrying:
        if type(obj).__name__ == 'balloon':
            balloon_count = balloon_count + 1

    if balloon_count >= 2:
        return True
