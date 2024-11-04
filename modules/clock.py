from core.lcd import POINTER
import utime
import machine
from core.beeper import menu_key, jump_melody
class Clock:
    def __init__(self, lcd, buttons, system, beeper):
        self.lcd = lcd
        self.buttons = buttons
        self.system = system
        self.beeper = beeper
        self.current_time = list(utime.localtime())
        self.selected_item = 0  # 0: back, 1: hours, 2: minutes
        self.items = ["Back", "HH", "MM"]

    def enter(self):
        self._update_menu_line()
        self._update_time_line()

    def update(self):
        self._update_time_line()

        # Handle button presses
        if self.buttons.is_pressed(self.buttons.down) and self.selected_item < len(self.items) - 1:
            self.beeper.play_melody(menu_key)
            self.selected_item = (self.selected_item + 1) % len(self.items)
            self._update_menu_line()
        elif self.buttons.is_pressed(self.buttons.up) and self.selected_item > 0:
            self.beeper.play_melody(menu_key)
            self.selected_item = (self.selected_item - 1) % len(self.items)
            self._update_menu_line()
        elif self.buttons.is_pressed(self.buttons.select):
            self.beeper.play_melody(jump_melody)
            self._handle_select()

    def _update_menu_line(self):
        # First line: Back, HH, MM with selection arrow
        first_line = " ".join([f"{POINTER if i == self.selected_item else ' '}{item}" for i, item in enumerate(self.items)])
        self.lcd.display(first_line, clear=False)
        
    def _update_time_line(self):
        self.current_time = list(utime.localtime())
        hour = f"{self.current_time[3]:02d}"
        minute = f"{self.current_time[4]:02d}"
        second = f"{self.current_time[5]:02d}"
        empty_padding = " " * ((self.lcd.I2C_NUM_COLS - len(hour) - len(minute) - len(second) - 2) // 2)
        second_line = f"{empty_padding}{hour}:{minute}:{second}"

        self.lcd.display_second_line(line2=second_line)

    def _handle_select(self):
        if self.selected_item == 0:  # Back
            self.system.back()
        elif self.selected_item == 1:  # Hours
            self.current_time[3] = (self.current_time[3] + 1) % 24
            self._set_time()
        elif self.selected_item == 2:  # Minutes
            self.current_time[4] = (self.current_time[4] + 1) % 60
            self._set_time()

    def _set_time(self):
        # (year, month, day, weekday, hours, minutes, seconds, subseconds)
        date = (self.current_time[0], self.current_time[1], self.current_time[2], self.current_time[6], self.current_time[3], self.current_time[4], 0, 0)
        machine.RTC().datetime(date)

    def exit(self):
        self.lcd.animated_clear()