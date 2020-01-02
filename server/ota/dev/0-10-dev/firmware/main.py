import config
from lib.ota import OTA
from lib.led import Led
from lib import effects, utils
from network import ftp, telnet
from lib.button import TouchHandler


def main():
    """Main function"""
    # Connect to wifi
    if config.Wifi.wifi:
        wifi = utils.wifi_connect(config.Wifi.ssid, config.Wifi.password)
        # Check firmware update
        if config.OTA.ota and wifi:
            ota = OTA(config.OTA)
            status = ota.check()
            if status:
                ota.update(status)
    # Start development servers
    if config.Servers.Ftp.ftp:
        ftp.start(user=config.Servers.Ftp.user, password=config.Servers.Ftp.password, buffsize=1024)
    if config.Servers.Telnet.telnet:
        telnet.start(user=config.Servers.Telnet.user, password=config.Servers.Telnet.password)
    # Init
    strip = Led(config.Led)
    touch = TouchHandler(config.Button)
    # Start effects
    effects.run(touch, strip)


main()
