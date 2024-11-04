from machine import Pin

class Buttons:
    def __init__(self):
        self.up = Pin(15, Pin.IN, Pin.PULL_DOWN)
        self.down = Pin(14, Pin.IN, Pin.PULL_DOWN)
        self.select = Pin(13, Pin.IN, Pin.PULL_DOWN)

    def is_pressed(self, button):
        return button.value() == 1
