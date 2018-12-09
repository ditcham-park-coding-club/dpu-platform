portable = True

sayings = ["I'm sad..."]


def on_frame(self, keystate):
    if sayings and self.speech is None:
        self.say(sayings.pop(0))
