import random

sayings = ["Grrr",
           "Circular people go home",
           "NO immigration",
           "I want a cupcake"]


def on_frame(self, key_state):
    if sayings and self.speech is None:
        self.say(random.choice(sayings))
