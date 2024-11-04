from machine import PWM, Pin, Timer

# Define note frequencies
NOTE_FREQUENCIES = {
    'C0': 33,
    'D0': 37,
    'E0': 41,
    'F0': 43,
    'G0': 49,
    'A0': 55,
    'B0': 62,
    'C1': 65,
    'D1': 73,
    'E1': 82,
    'F1': 87,
    'G1': 98,
    'A1': 110,
    'B1': 123,
    'C2': 131,
    'D2': 147,
    'E2': 165,
    'F2': 175,
    'G2': 196,
    'A2': 220,
    'B2': 247,
    'C3': 131,
    'D3': 196,
    'E3': 220,
    'F3': 247,
    'G3': 294,
    'A3': 349,
    'B3': 392,
    'C4': 261,
    'D4': 294,
    'E4': 329,
    'F4': 349,
    'G4': 392,
    'A4': 440,
    'B4': 494,
    'C5': 523,
    'D5': 587,
    'E5': 659,
    'F5': 698,
    'G5': 784,
    'A5': 880,
    'B5': 988,
    'C6': 1047,
    'D6': 1175,
    'E6': 1319,
    'F6': 1397,
    'G6': 1568,
    'A6': 1760,
    'B6': 1976,
}

menu_key = [
    ('E3', 90), ('PAUSE', 30), ('A3', 50)
]
select_melody = [
    ('A4', 100), ('PAUSE', 90), ('A4', 50)
]
enter_melody = [
    ('C4', 100), ('PAUSE', 90), ('D4', 100), ('PAUSE', 90), ('F4', 250)
]
exit_melody = [
    ('B4', 100), ('PAUSE', 90), ('A4', 100), ('PAUSE', 90), ('G3', 250)
]
jump_melody = [
    ('B4', 100)
]

class Beeper:
    VOLUME_LEVELS = [0, 13107, 26214, 39321, 52428, 65535]  # Define 6 volume levels

    def __init__(self, pin_number):
        self.pwm = PWM(Pin(pin_number))
        self.pwm.duty_u16(0)  # Start with no sound
        self.timer = Timer()
        self.current_volume_level = 1  # Default to medium volume
        self.melody = [] # List of notes to play
        self.current_note_index = 0 # Index of the current note to play

    def increase_volume(self):
        if self.current_volume_level < len(self.VOLUME_LEVELS) - 1:
            self.current_volume_level += 1

    def decrease_volume(self):
        if self.current_volume_level > 0:
            self.current_volume_level -= 1

    def play_melody(self, melody):
        self.melody = melody
        self.current_note_index = 0
        self._play_next_note(None)

    def _play_next_note(self, t):
        if self.current_note_index < len(self.melody):
            note_name, duration = self.melody[self.current_note_index]
            if note_name == 'PAUSE':
                self._stop_tone(None)  # Ensure no sound is played
            else:
                frequency = NOTE_FREQUENCIES.get(note_name, 0)
                if frequency > 0:
                    self._play_tone(frequency, duration)
            self.current_note_index += 1
            self.timer.init(period=duration, mode=Timer.ONE_SHOT, callback=self._play_next_note)
        else:
            self._stop_tone(None)
    
    def _play_tone(self, frequency, duration):
        volume = self.VOLUME_LEVELS[self.current_volume_level]
        self.pwm.freq(frequency)
        self.pwm.duty_u16(volume)
        # Use a timer to stop the sound after the duration
        self.timer.init(period=duration, mode=Timer.ONE_SHOT, callback=self._stop_tone)

    def _stop_tone(self, t):
        self.pwm.duty_u16(0)
        self.timer.deinit()