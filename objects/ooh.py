from setup import object_group

def on_frame(self, keystate):
    anything_is_a_box = False
    for obj in object_group:
        if type(obj).__name__ == 'box':
            anything_is_a_box = True

    if not anything_is_a_box:
        self.say("I'm sad...")
