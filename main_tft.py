from boot import SSID
from sysfont import sysfont
from ST7735 import TFT
from machine import SPI, Pin

spi = SPI(
    2,
    baudrate=20000000,
    polarity=0,
    phase=0,
    sck=Pin(14),
    mosi=Pin(13),
    miso=Pin(12)
)
tft = TFT(spi, 16, 17, 18)
tft.initb2()
tft.rgb(True)
tft.fill(TFT.BLACK)
tft.fillrect((0, 0), (128, 40), TFT.FOREST)
tft.fillrect((0, 40), (128, 160), TFT.GREEN)
tft.text((2, 2), "Wifi: " + SSID, TFT.NAVY, sysfont, 1.1, nowrap=False)
tft.text((2, 10), "NodeType: " + 'SPRINKLER', TFT.NAVY, sysfont, 1.1, nowrap=False)
tft.text((2, 20), "Api Gateway:", TFT.NAVY, sysfont, 1.1, nowrap=False)
tft.text((2, 30), "192.168.20.125:8080", TFT.NAVY, sysfont, 1, nowrap=False)
