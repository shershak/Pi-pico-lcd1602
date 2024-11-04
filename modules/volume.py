from core.beeper import menu_key, jump_melody

class Volume:
    def __init__(self, lcd, buttons, beeper, system):
        self.lcd = lcd
        self.buttons = buttons
        self.beeper = beeper
        self.system = system
        
    def enter(self):
        self.display()
      
    def exit(self):
        pass
      
    def display(self):
        level = self.beeper.current_volume_level
        self.lcd.display_volume(level)

    def update(self):
        if self.buttons.is_pressed(self.buttons.up) and self.beeper.current_volume_level < len(self.beeper.VOLUME_LEVELS) - 1:
            self.beeper.increase_volume()
            self.display()
            self.beeper.play_melody(menu_key)  # Play test tone
        elif self.buttons.is_pressed(self.buttons.down) and self.beeper.current_volume_level > 0:
            self.beeper.decrease_volume()
            self.display()
            self.beeper.play_melody(menu_key)  # Play test tone
        elif self.buttons.is_pressed(self.buttons.select):
            self.beeper.play_melody(jump_melody)
            self.system.back()
