from core.lcd import POINTER
from core.beeper import menu_key, select_melody

class FeatureItem:
    FILE_EXPLORER = "File Explorer"
    CLOCK = "Time"
    GAME = "Dino Game"
    DOC = "Doc"
    MENU = "Menu"
    LED = "LED"
    VOLUME = "Volume"

class Menu:
    def __init__(self, lcd, buttons, system, menu_items, beeper):
        self.lcd = lcd
        self.buttons = buttons
        self.system = system
        self.menu_items = menu_items  # List of (name, feature_instance)
        self.selected = 0
        self.beeper = beeper

    def enter(self):
        self.display()

    def display(self):
        # Display menu options.
        name = self.menu_items[self.selected][0]
        first_line = f"{POINTER} {name}"
        second_line = f"  {self.menu_items[self.selected + 1][0] if self.selected + 1 < len(self.menu_items) else ''}"
        self.lcd.display(first_line, second_line)

    def update(self):
        # Handle navigation and selection with buttons.
        if self.buttons.is_pressed(self.buttons.up) and self.selected > 0:
            self.beeper.play_melody(menu_key)
            self.selected = (self.selected - 1) % len(self.menu_items)
            self.display()
        elif self.buttons.is_pressed(self.buttons.down) and self.selected < len(self.menu_items) - 1:
            self.beeper.play_melody(menu_key)
            self.selected = (self.selected + 1) % len(self.menu_items)
            self.display()
        elif self.buttons.is_pressed(self.buttons.select):
            self.beeper.play_melody(select_melody)
            _, feature = self.menu_items[self.selected]
            self.system.switch_to(feature)  # Switch to the selected feature

    def exit(self):
        pass
      


