import utime
from machine import PWM, Pin
from core.lcd import LCD
from core.buttons import Buttons
from core.beeper import Beeper
from system import System
from modules.file_explorer import FileExplorer
from modules.clock import Clock
from modules.dino_game import Game
from modules.doc import Doc
from modules.menu import FeatureItem, Menu
from modules.led import LED
from modules.volume import Volume

# Constants
DEBOUNCE_DELAY = 100  # milliseconds

def initialize_system():
    # Initialize core components
    lcd = LCD()
    buttons = Buttons()
    beeper = Beeper(9)

    # Initialize system
    system = System(lcd, buttons, None, None)  # Pass None for menu and doc initially

    # Create feature instances with system reference
    file_explorer = FileExplorer(lcd, buttons, system, beeper)
    clock = Clock(lcd, buttons, system, beeper)
    game = Game(lcd, buttons, system, beeper)
    doc = Doc(lcd, buttons, system)
    led = LED(lcd, buttons, system, beeper)
    volume = Volume(lcd, buttons, beeper, system)
    # Define menu items as (name, feature_instance)
    menu_items = [
        (FeatureItem.FILE_EXPLORER, file_explorer),
        (FeatureItem.CLOCK, clock),
        (FeatureItem.GAME, game),
        (FeatureItem.LED, led),
        (FeatureItem.VOLUME, volume),
    ]

    # Initialize menu with system reference
    menu = Menu(lcd, buttons, system, menu_items, beeper)

    # Set menu and doc in system
    system.menu = menu # type: ignore
    system.doc = doc # type: ignore

    return system

def main():
    system = initialize_system()
    # Start with the main menu
    system.switch_to(FeatureItem.MENU)

    # Main loop
    while True:
        try:
            system.update()  # Update the active feature
            utime.sleep_ms(DEBOUNCE_DELAY)  # Debounce delay
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
