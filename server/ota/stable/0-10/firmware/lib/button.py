import time
import _thread
from machine import Pin, TouchPad


class TouchHandler:
    """Class for handle touch buttons"""

    def __init__(self, config):
        # Setup touch
        self.button = TouchPad(Pin(config.button))
        # Calibrate
        self.threshold = self.calibrate()
        # State vars
        self.state = None
        # Run all threads
        self.start_threads()

    def __button_th__(self):
        """button_thread"""
        while True:
            val = self.button.read()
            cap_ratio = val / self.threshold
            # Check if a TouchPad is pressed
            if 0.40 < cap_ratio < 0.95:
                self.state = "short"
                time.sleep(0.2)  # Debounce press
            time.sleep(0.01)
            self.state = None

    def calibrate(self):
        """Calibrates touchpad"""
        threshold = []
        # Get touchpad noise
        for x in range(12):
            threshold.append(self.button.read())
            time.sleep(0.1)
        # Store sums of all noise
        threshold_int = sum(threshold) // len(threshold)
        return threshold_int

    def start_threads(self):
        """Starts threads"""
        try:
            _thread.start_new_thread("__button_th__", self.__button_th__, ())
        except Exception as e:
            print("Something went wrong! Error: ", e)
