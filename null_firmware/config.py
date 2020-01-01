# Standard config file for ESP32

class Wifi:
    """Wifi settings"""
    wifi = True
    ssid = "ssid"
    password = "password"

class OTA:
    """Automatic updates"""
    ota = True
    branch = "stable"
    server_url = "https://ophoperhpo.github.io/neoled/"

class Servers:
    """Servers"""
    class Telnet:
        """Telnet"""
        telnet = False
        user = "$DAWDWDA$"
        password = "RAW@DAFAWD@"
    class Ftp:
        """Ftp"""
        ftp = False
        user = "FTPDRADAWD"
        password = "Fdfga24@@@@@D"

class Led:
    """Neopixel settings"""
    pin = 13
    pixels = 16
    type = "RGB"
    brightness = 255

class Button:
    """Buttons settings"""
    button = 4
