# Neopixel led control object
# Developed by Anodev Development (OPHoperHPO) (https://github.com/OPHoperHPO)
import time
import machine

class Led:
    """Led wrapper"""
    def __init__(self, config):
        """Init led"""
        # Parse vars from config
        pin = machine.Pin(int(config.pin))
        self.pixels = int(config.pixels)+1
        # Check led type
        if config.type == "RGB":
            type = machine.Neopixel.TYPE_RGB
        else:
            type = machine.Neopixel.TYPE_RGBW
        # Init led
        self.led = machine.Neopixel(pin, self.pixels, type)
        # Set brightness
        self.led.brightness(config.brightness, True)
        # Clear Led
        self.led.clear()

    @staticmethod
    def rgb2int(color:list):
        rgb = (65536 * color[0]) + (256 * color[1]) + color[2]
        return rgb

    def set_all_clr(self, color, delay=0.01):
        """Sets all pixels to specified color"""
        for i in range(self.pixels):
            self.led.set(i, self.rgb2int(color), update=True)
            time.sleep(delay)

    def set_one(self, num, color):
        """Sets one pixel to specified color"""
        self.led.set(num, self.rgb2int(color), update=True)

    def __del__(self):
        self.led.clear()
        self.led.deinit()
