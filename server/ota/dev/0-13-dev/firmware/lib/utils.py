# Standard utils file
# Developed by Anodev Development (OPHoperHPO) (https://github.com/OPHoperHPO)
import time
import network


def wifi_connect(SSID, PASSWORD):
    """Connects to wifi."""
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        timer = 30
        while not sta_if.isconnected():
            if timer == 0 and sta_if.isconnected() is False:
                return False
            time.sleep(1)
            timer -= 1
    print('Network config:', sta_if.ifconfig())
    return sta_if
