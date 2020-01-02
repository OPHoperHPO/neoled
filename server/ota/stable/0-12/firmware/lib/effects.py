# Neopixel led effects + interface
# Developed by Anodev Development (OPHoperHPO) (https://github.com/OPHoperHPO)
import time
import random as rnd

def init(strip):
    strip.set_all_clr(color=[100, 0, 50], delay=0.01)


def clear(strip):
    strip.set_all_clr(color=[128, 0, 0], delay=0.01)

def run(touch, strip):
    init(strip)
    while True:
        rainbow(touch, strip)
        fade_red(touch, strip)
        fade_blue(touch, strip)
        fade_green(touch, strip)
        white_cycle(touch, strip)
        blue_bounce(touch, strip)
        random_cycle(touch, strip)
        rainbow_fast(touch, strip)
        white(touch, strip)
        red(touch, strip)
        green(touch, strip)
        purple(touch, strip)
        yellow(touch, strip)
        blue(touch, strip)
        random_color(touch, strip)
        random_smart(touch, strip)
        sleep(touch, strip)


def check_button(touch):
    if touch.state == "short":
        time.sleep(0.7)
        return 1
    else:
        return 0


def rainbow(touch, strip, loops=12000000, delay=0.1, sat=1.0, bri=0.4):
    for pos in range(0, loops):
        if check_button(touch) == 1:
            return 0
        for i in range(0, strip.pixels):
            dHue = 360.0 / 24 * (pos + i)
            hue = dHue % 360
            strip.led.setHSB(i, hue, sat, bri, 1, False)
        strip.led.show()
        if delay > 0:
            time.sleep(delay)


def rainbow_fast(touch, strip, loops=12000000, delay=0.05, sat=1.0, bri=0.4):
    for pos in range(0, loops):
        if check_button(touch) == 1:
            return 0
        for i in range(0, strip.pixels):
            dHue = 360.0 / 24 * (pos + i)
            hue = dHue % 360
            strip.led.setHSB(i, hue, sat, bri, 1, False)
        strip.led.show()
        if delay > 0:
            time.sleep(delay)


def fade_red(touch, ld, delay=0.01):
    while True:
        if check_button(touch) == 1:
            return 0
        for color in range(0, 255):
            if check_button(touch) == 1:
                return 0
            for pixel in range(0, ld.pixels):
                ld.led.set(pixel, ld.rgb2int([color, 0, 0]), update=False)
            ld.led.show()
            time.sleep(delay)
        for color in reversed(range(0, 255)):
            if check_button(touch) == 1:
                return 0
            for pixel in range(0, ld.pixels):
                ld.led.set(pixel, ld.rgb2int([color, 0, 0]), update=False)
            ld.led.show()
            time.sleep(delay)


def fade_green(touch, ld, delay=0.01):
    while True:
        if check_button(touch) == 1:
            return 0
        for color in range(0, 255):
            if check_button(touch) == 1:
                return 0
            for pixel in range(0, ld.pixels):
                ld.led.set(pixel, ld.rgb2int([0, color, 0]), update=False)
            ld.led.show()
            time.sleep(delay)
        for color in reversed(range(0, 255)):
            if check_button(touch) == 1:
                return 0
            for pixel in range(0, ld.pixels):
                ld.led.set(pixel, ld.rgb2int([0, color, 0]), update=False)
            ld.led.show()
            time.sleep(delay)


def fade_blue(touch, ld, delay=0.01):
    while True:
        if check_button(touch) == 1:
            return 0
        for color in range(0, 255):
            if check_button(touch) == 1:
                return 0
            for pixel in range(0, ld.pixels):
                ld.led.set(pixel, ld.rgb2int([0, 0, color]), update=False)
            ld.led.show()
            time.sleep(delay)
        for color in reversed(range(0, 255)):
            if check_button(touch) == 1:
                return 0
            for pixel in range(0, ld.pixels):
                ld.led.set(pixel, ld.rgb2int([0, 0, color]), update=False)
            ld.led.show()
            time.sleep(delay)


def blue(touch, ld):
    ld.set_all_clr([0, 0, 255], delay=0.05)
    while True:
        time.sleep(0.2)
        if check_button(touch) == 1:
            return 0


def green(touch, ld):
    ld.set_all_clr([0, 255, 0], delay=0.05)
    while True:
        time.sleep(0.2)
        if check_button(touch) == 1:
            return 0


def red(touch, ld):
    ld.set_all_clr([255, 0, 0], delay=0.05)
    while True:
        time.sleep(0.2)
        if check_button(touch) == 1:
            return 0


def purple(touch, ld):
    ld.set_all_clr([255, 0, 255], delay=0.05)
    while True:
        time.sleep(0.2)
        if check_button(touch) == 1:
            return 0


def yellow(touch, ld):
    ld.set_all_clr([255, 255, 0], delay=0.05)
    while True:
        time.sleep(0.2)
        if check_button(touch) == 1:
            return 0


def random_color(touch, ld):
    ld.set_all_clr([rnd.randint(0, 255), rnd.randint(0, 255), rnd.randint(0, 255)], delay=0.05)
    while True:
        time.sleep(0.2)
        if check_button(touch) == 1:
            return 0


def random_smart(touch, ld):
    num = rnd.randint(1, 3)
    if num == 1:
        num2 = rnd.randint(1, 3)
        if num2 == 1:
            ld.set_all_clr([rnd.randint(0, 255), 0, 0], delay=0.05)
        if num2 == 2:
            ld.set_all_clr([0, rnd.randint(0, 255), 0], delay=0.05)
        if num2 == 3:
            ld.set_all_clr([0, 0, rnd.randint(0, 255)], delay=0.05)
    if num == 2:
        num2 = rnd.randint(1, 3)
        if num2 == 1:
            ld.set_all_clr([rnd.randint(0, 255), 0, rnd.randint(0, 255)], delay=0.05)
        if num2 == 2:
            ld.set_all_clr([rnd.randint(0, 255), rnd.randint(0, 255), 0], delay=0.05)
        if num2 == 3:
            ld.set_all_clr([0, rnd.randint(0, 255), rnd.randint(0, 255)], delay=0.05)
    while True:
        time.sleep(0.2)
        if check_button(touch) == 1:
            return 0


def white(touch, ld):
    ld.set_one(0, [100, 100, 100])
    ld.set_one(2, [100, 100, 100])
    ld.set_one(4, [100, 100, 100])
    while True:
        time.sleep(0.2)
        if check_button(touch) == 1:
            return 0


def white_cycle(touch, ld):
    while True:
        if check_button(touch) == 1:
            return 0
        for i in range(4 * ld.pixels):
            if check_button(touch) == 1:
                return 0
            for j in range(ld.pixels):
                ld.led.set(j, ld.rgb2int([0, 0, 0]), update=False)
            ld.led.set(i % ld.pixels, ld.rgb2int([255, 255, 255]), update=False)
            ld.led.show()
            time.sleep(0.1)


def blue_bounce(touch, ld):
    n = ld.pixels
    while True:
        if check_button(touch) == 1:
            return 0
        for i in range(4 * n):
            if check_button(touch) == 1:
                return 0
            for j in range(n):
                ld.led.set(j, ld.rgb2int([0, 0, 128]), update=False)
            if (i // n) % 2 == 0:
                ld.led.set(i % n, ld.rgb2int([0, 0, 0]), update=False)
            else:
                ld.led.set(n - 1 - (i % n), ld.rgb2int([0, 0, 0]), update=False)
            ld.led.show()
            time.sleep(0.060)


def sleep(touch, ld):
    ld.set_all_clr([0, 0, 20], delay=0.05)
    while True:
        time.sleep(0.2)
        if check_button(touch) == 1:
            return 0


def random_cycle(touch, ld):
    while True:
        if check_button(touch) == 1:
            return 0
        for pixel in range(ld.pixels):
            if check_button(touch) == 1:
                return 0
            ld.set_one(pixel, [rnd.randint(0, 70), rnd.randint(0, 50), rnd.randint(0, 70)])
            time.sleep(0.1)
