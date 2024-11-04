from modules.menu import FeatureItem

class Doc:
    def __init__(self, lcd, buttons, system):
        self.lcd = lcd
        self.buttons = buttons
        self.system = system
        self.file_content = ""
        self.lines = []
        self.current_line = 0

    def enter(self, file_path):
        self.file_content = self._read_file(file_path)
        self.lines = self._get_lines(self.file_content)
        self.lcd.display_doc(self.lines, self.current_line)

    def update(self):
        if self.buttons.is_pressed(self.buttons.up) and self.current_line > 0:
            self.current_line -= 1
            self.lcd.display_doc(self.lines, self.current_line)

        if self.buttons.is_pressed(self.buttons.down) and self.current_line < len(self.lines) - 2:
            self.current_line += 1
            self.lcd.display_doc(self.lines, self.current_line)

        if self.buttons.is_pressed(self.buttons.select):
            self.system.back()

    def exit(self):
        self.file_content = ""
        self.lines = []
        self.current_line = 0
        self.lcd.animated_clear()

    def _read_file(self, file_path):
        with open(file_path, 'r') as file:
            return file.read()
    
    def _get_lines(self, text):
        num_cols = self.lcd.I2C_NUM_COLS - 1
        lines = []
        i = 0

        while i < len(text):
            end = i + num_cols
            line = text[i:end]
            
            if end < len(text) and text[end] != ' ' and text[end - 1] != ' ':
                last_space = line.rfind(' ')
                if last_space != -1:
                    end = i + last_space
                    line = text[i:end]
                    i = end + 1
                else:
                    if len(line) == num_cols:
                        i = end
                    else:
                        next_space = text.find(' ', end)
                        if next_space != -1:
                            line = text[i:next_space]
                            i = next_space + 1
                        else:
                            line = text[i:]
                            i = len(text)
            else:
                i = end

            line = line.lstrip()

            if len(line) < num_cols:
                line += ' ' * (num_cols - len(line))

            lines.append(line)

        return lines
