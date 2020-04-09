"""
 NodeMCU ESP8266 Cooling system device node
 Author Shanmugathas Vigneswaran
"""
import network

SSID = 'raspi-webgui'
PASSWORD = 'ChangeMe'


def connect_access_point():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(SSID, PASSWORD)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


if __name__ == '__main__':
    connect_access_point()
