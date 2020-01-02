# Rescue tools for recover esp32 in short time.
import network

def wifi_connect():
    """Connects to wifi."""
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('Connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print('Network config:', sta_if.ifconfig())

def start_rescue_servers():
    """Connects to wifi."""
    # Start telnet server
    network.telnet.start(user=RESCUE_USER, password=RESCUE_PASSWORD)
    # Start ftp server
    network.ftp.start(user=RESCUE_USER, password=RESCUE_PASSWORD, buffsize=1024, timeout=300)

# INIT vars
SSID = input("WIFI SSID: ")
PASSWORD = input("WIFI PASSWORD: ")
RESCUE_USER = input("RESCUE USER: ")
RESCUE_PASSWORD = input("RESCUE PASSWORD: ")

wifi_connect()
start_rescue_servers()
