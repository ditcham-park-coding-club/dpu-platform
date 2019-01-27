# Make self.hit_by


def on_frame(self, key_state, level):
    if self.hit is not None and self.hit.type_name == 'Fudge Jumping':
        self.say('Game Over')
        self.hit.kill()
