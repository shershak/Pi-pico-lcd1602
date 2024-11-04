from machine import I2C, Pin
from core.pico_i2c_lcd import I2cLcd
import utime

POINTER = '>'
DINO_1 = '%'
DINO_2 = '$'
OBSTACLE_1 = '^'
OBSTACLE_2 = '&'
FILE = '$'
PLUS = '+'
MINUS = '-'


class LCD:
    I2C_ADDR = 0x27
    I2C_NUM_ROWS = 2
    I2C_NUM_COLS = 16
    arrow_right_char = [0x00, 0x00, 0x08, 0x0C, 0x0E, 0x0C, 0x08, 0x00]
    arrow_down_char = [0x00, 0x00, 0x00, 0x1F, 0x0E, 0x04, 0x00, 0x00]
    folder_char = [0x00, 0x00, 0x18, 0x17, 0x11, 0x11, 0x1F, 0x00]
    file_char = [0x00, 0x07, 0x09, 0x11, 0x11, 0x11, 0x1F, 0x00]
    full_char = [0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F, 0x1F]
    
    dino_1_char = [  0x00, 0x01, 0x11, 0x1B, 0x0F, 0x07, 0x02, 0x03]
    dino_2_char = [0x1E, 0x17, 0x1F, 0x18, 0x1C, 0x14, 0x10, 0x18]
    obstacle_1_char = [0x00, 0x04, 0x04, 0x15, 0x15, 0x1F, 0x04, 0x04]
    obstacle_2_char = [0x00,0x00,0x00,0x04,0x05,0x15,0x1E,0x04]

    def __init__(self):
        i2c = I2C(0, scl=Pin(1), sda=Pin(0))
        self.lcd = I2cLcd(i2c, self.I2C_ADDR, self.I2C_NUM_ROWS, self.I2C_NUM_COLS)
        self._dino_chars_set = False
        self._full_char_set = False
        self._tree_chars_set = False

    def display(self, line1, line2="", clear=True):
        if clear:
            self.lcd.clear()

        # Ensure line1 and line2 are strings
        line1 = str(line1)
        line2 = str(line2)

        self.lcd.move_to(0, 0)
        if len(line1) > self.I2C_NUM_COLS:
            line1 = line1[:self.I2C_NUM_COLS]
        else:
            line1 = self._pad_string(line1, self.I2C_NUM_COLS)
        self.lcd.putstr(line1)

        if line2:
            self.lcd.move_to(0, 1)
            if len(line2) > self.I2C_NUM_COLS:
                line2 = line2[:self.I2C_NUM_COLS]
            else:
                line2 = self._pad_string(line2, self.I2C_NUM_COLS)
            self.lcd.putstr(line2)

    def display_second_line(self, line2):
        line2 = str(line2)

        # Function to pad strings to a specific length
        def pad_string(s, length):
            return s + ' ' * (length - len(s))

        self.lcd.move_to(0, 1)
        if len(line2) > self.I2C_NUM_COLS:
            line2 = line2[:self.I2C_NUM_COLS]
        else:
            line2 = pad_string(line2, self.I2C_NUM_COLS)
        self.lcd.putstr(line2)

    def display_tree(self, line1, line2):
        if not self._tree_chars_set:
            self.lcd.custom_char(5, bytearray(self.folder_char))
            self.lcd.custom_char(6, bytearray(self.file_char))
            self.lcd.custom_char(2, bytearray(self.arrow_right_char))
            self.lcd.custom_char(3, bytearray(self.arrow_down_char))
            self._tree_chars_set = True

        def replace_special_symbols(line):
          line = line.replace(FILE, '\x06')  # file icon
          line = line.replace(PLUS, '\x02')
          line = line.replace(MINUS, '\x03')
          return line
        
        self.display(replace_special_symbols(line1), replace_special_symbols(line2), clear=False)

    def display_doc(self, lines, current_line):
        self.lcd.clear()
        self.lcd.move_to(0, 0)
        self.lcd.putstr(lines[current_line])
        if len(lines) > 1:
            self.lcd.move_to(0, 1)
            self.lcd.putstr(lines[current_line + 1])
        
        if len(lines) > 2:
            text_percent = current_line * 100 / (len(lines) - 2)
            
            # Create the scroll bar for both rows
            scroll_list = [0x00] * 16
            
            # Determine the scroll position (0 to 13) based on the percentage
            scroll_position = int(text_percent / 100 * 12)
            
            # Adjust the scroll bar position
            for i in range(4):
                if scroll_position + i < len(scroll_list):
                    scroll_list[scroll_position + i] = 0x03

            scroll = bytearray(scroll_list)
            
            # Load the custom character for the scroll bar
            self.lcd.custom_char(0, scroll[0:8])
            self.lcd.custom_char(1, scroll[8:16])
            
            # Display the scroll indicator in the last column of both rows
            self.lcd.move_to(15, 0)
            self.lcd.putchar(chr(0))
            self.lcd.move_to(15, 1)
            self.lcd.putchar(chr(1))

    def animated_clear(self, delay_ms=50):
        if not self._full_char_set:
            self.lcd.custom_char(7, bytearray(self.full_char))
            self._full_char_set = True

        # animation to the center
        for col in range(self.I2C_NUM_COLS // 2):
            left_col = col
            right_col = self.I2C_NUM_COLS - col - 1
            for row in range(self.I2C_NUM_ROWS):
                self.lcd.move_to(left_col, row)
                self.lcd.putchar(chr(7))
                self.lcd.move_to(right_col, row)
                self.lcd.putchar(chr(7))
            utime.sleep_ms(delay_ms)
        # animation from the center
        for col in range(self.I2C_NUM_COLS // 2):
            left_col = (self.I2C_NUM_COLS // 2) - 1 - col
            right_col = (self.I2C_NUM_COLS // 2) + col
            for row in range(self.I2C_NUM_ROWS):
                self.lcd.move_to(left_col, row)
                self.lcd.putchar(' ')
                self.lcd.move_to(right_col, row)
                self.lcd.putchar(' ')
            utime.sleep_ms(delay_ms)

    def display_dino_game(self, line1, line2):
        if not self._dino_chars_set:
            self.lcd.custom_char(5, bytearray(self.dino_1_char))
            self.lcd.custom_char(6, bytearray(self.dino_2_char))
            self.lcd.custom_char(2, bytearray(self.obstacle_1_char))
            self.lcd.custom_char(3, bytearray(self.obstacle_2_char))
            self._dino_chars_set = True
            
        def replace_special_symbols(line):
          line = line.replace(DINO_1, '\x05')  # dino 1
          line = line.replace(DINO_2, '\x06')  # dino 2
          line = line.replace(OBSTACLE_1, '\x02')  # obstacle 1
          line = line.replace(OBSTACLE_2, '\x03')  # obstacle 2
          return line

        self.display(replace_special_symbols(line1), replace_special_symbols(line2), clear=False)
        
    def display_volume(self, level):
        self.display(f"{POINTER} Back", f"  Volume: {level}", clear=False)
        
    def reset_custom_chars(self):
        self._dino_chars_set = False
        self._full_char_set = False
        self._tree_chars_set = False
        
    # function to pad strings to a specific length
    def _pad_string(self, s, length):
        return s + ' ' * (length - len(s))
      

