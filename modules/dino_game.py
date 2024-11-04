from core.lcd import DINO_1, DINO_2, OBSTACLE_1, OBSTACLE_2
import utime
import random
from core.beeper import jump_melody, exit_melody
MAX_OBSTACLES = 3
OBSTACLE_INTERVAL = 10
OBSTACLES = 15

class Game:
    def __init__(self, lcd, buttons, system, beeper):
        self.lcd = lcd
        self.buttons = buttons
        self.system = system
        self.beeper = beeper
        
        # Initialize game variables
        self.dino_position = 0
        self.is_jumping = False
        self.score = 0
        self.jump_length = 4 # Maximum jump length
        self.current_jump_length = 0 # Current jump length counter
        self.obstacles = [OBSTACLES]  # List to hold obstacle positions
        self.obstacle_chars = [OBSTACLE_1]  # Initialize with a default character
        self.max_obstacles = MAX_OBSTACLES  # Maximum number of obstacles on screen
        self.obstacle_interval = OBSTACLE_INTERVAL  # Interval between obstacles

    def enter(self):
        dino_start_line_1 = f"Start Game!"
        dino_start_line_2 = f"{DINO_1}{DINO_2}       {OBSTACLE_1}    {OBSTACLE_2}"
        dino_start_empty_space = (self.lcd.I2C_NUM_COLS - len(dino_start_line_1)) // 2
        dino_start_line_2_empty_space = (self.lcd.I2C_NUM_COLS - len(dino_start_line_2)) // 2
        line_1 = f"{dino_start_empty_space * ' '}{dino_start_line_1}"
        line_2 = f"{dino_start_line_2_empty_space * ' '}{dino_start_line_2}"

        self.lcd.display_dino_game(line_1, line_2)
        utime.sleep_ms(1500)
        self.lcd.animated_clear()

    def update(self):
        while True:
            # Check for jump
            if self.buttons.is_pressed(self.buttons.up):
                self.beeper.play_melody(jump_melody)
                self.is_jumping = True
            
            # Check for exit
            if self.buttons.is_pressed(self.buttons.select):
                self.system.back()
                break

            self._update_game_state()
            self._display_game_state()

            if self._obstacle_collision():
                break

            # Delay for game speed
            # utime.sleep_ms(50)

    def _update_game_state(self):
        # Move obstacles
        for i in range(len(self.obstacles)):
            self.obstacles[i] -= 1
            if self.obstacles[i] < 0:
                self.obstacles[i] = self.obstacle_interval * (self.max_obstacles - 1)
                self.score += 1
                self.obstacle_chars[i] = [OBSTACLE_1, OBSTACLE_2][random.getrandbits(1)]  # Assign new character

        # Add new obstacle if needed
        if len(self.obstacles) < self.max_obstacles and self.obstacles[-1] < self.obstacle_interval:
            self.obstacles.append(self.obstacle_interval * (self.max_obstacles - 1))
            self.obstacle_chars.append([OBSTACLE_1, OBSTACLE_2][random.getrandbits(1)])  # Assign character to new obstacle

        # Handle jump
        if self.is_jumping:
            if self.current_jump_length < self.jump_length:
                self.dino_position = 1  # Dino is "jumping"
                self.current_jump_length += 1
            else:
                self.is_jumping = False
                self.current_jump_length = 0
        else:
            self.dino_position = 0  # Dino is on the ground

    def _display_game_state(self):
        # Display the dino and obstacles
        obstacle_char = [' '] * self.lcd.I2C_NUM_COLS

        for i, pos in enumerate(self.obstacles):
            if i < len(self.obstacle_chars) and 0 <= pos < self.lcd.I2C_NUM_COLS:
                obstacle_char[pos] = self.obstacle_chars[i]  # Use stored character

        # Create the display strings
        dino = str(DINO_1 + DINO_2) if self.dino_position == 1 else ''
        first_line_space = self.lcd.I2C_NUM_COLS - len(dino) - len(str(self.score))
        first_line = dino + (' ' * first_line_space) + str(self.score)

        # Adjust dino position display logic
        if self.dino_position == 0:
            obstacle_char[0] = DINO_1
            obstacle_char[1] = DINO_2
        else:
            if DINO_1 in obstacle_char:
                obstacle_char[obstacle_char.index(DINO_1)] = ' '
            if DINO_2 in obstacle_char:
                obstacle_char[obstacle_char.index(DINO_2)] = ' '

        second_line = ''.join(obstacle_char)
        self.lcd.display_dino_game(first_line, second_line)
        
    def _obstacle_collision(self):
        for pos in self.obstacles:
            if (pos == 1 or pos == 0) and self.dino_position == 0:
                game_over = "Game Over!"
                first_line_space = (self.lcd.I2C_NUM_COLS - len(game_over)) // 2
                score = f"Score: {self.score}"
                second_line_space = (self.lcd.I2C_NUM_COLS - len(score)) // 2
                self.lcd.display(f"{first_line_space * ' '}{game_over}", f"{second_line_space * ' '}{score}")
                self.beeper.play_melody(exit_melody)
                utime.sleep_ms(2000)
                self.system.back()
                return True
        return False

    def exit(self):
        self.score = 0
        self.dino_position = 0
        self.obstacles = [OBSTACLES]
        self.max_obstacles = MAX_OBSTACLES
        self.obstacle_chars = [OBSTACLE_1]
        self.lcd.animated_clear()
