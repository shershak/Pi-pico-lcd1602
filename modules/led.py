from core.lcd import POINTER
from machine import Pin
from core.beeper import jump_melody, menu_key

class LEDItem:
    BACK = 0
    ON = 1
    OFF = 2
    YELLOW = 3
    BLUE = 4

led_items = [
    (LEDItem.BACK, "Back"),
    (LEDItem.ON, "On"),
    (LEDItem.OFF, "Off"),
    (LEDItem.YELLOW, "Yellow"),
    (LEDItem.BLUE, "Blue"),
]

class LED:
    def __init__(self, lcd, buttons, system, beeper):
        self.lcd = lcd
        self.buttons = buttons
        self.system = system
        self.beeper = beeper
        self.yellow_led = Pin(12, Pin.OUT)
        self.blue_led = Pin(11, Pin.OUT)
        self.selected = 0

    def enter(self):
        self._display_options()
        
    def update(self):
        if self.buttons.is_pressed(self.buttons.up) and self.selected > 0:
            self.beeper.play_melody(menu_key)
            self.selected = (self.selected - 1) % len(led_items)
            self._display_options()
        elif self.buttons.is_pressed(self.buttons.down) and self.selected < len(led_items) - 1:
            self.beeper.play_melody(menu_key)
            self.selected = (self.selected + 1) % len(led_items)
            self._display_options()
        elif self.buttons.is_pressed(self.buttons.select):
            self.beeper.play_melody(jump_melody)
            if led_items[self.selected][0] == LEDItem.ON:
                self.yellow_led.on()
                self.blue_led.on()
            elif led_items[self.selected][0] == LEDItem.OFF:
                self.yellow_led.off()
                self.blue_led.off()
            elif led_items[self.selected][0] == LEDItem.YELLOW:
                self.yellow_led.on()
                self.blue_led.off()
            elif led_items[self.selected][0] == LEDItem.BLUE:
                self.yellow_led.off()
                self.blue_led.on()
            elif led_items[self.selected][0] == LEDItem.BACK:
                self.system.back()

    def exit(self):
        self.yellow_led.off()
        self.blue_led.off()
        self.selected = 0
        
    def _display_options(self):
        name = led_items[self.selected][1]
        first_line = f"{POINTER} {name}"
        second_line = f"  {led_items[self.selected + 1][1] if self.selected + 1 < len(led_items) else ''}"
        self.lcd.display(first_line, second_line)
