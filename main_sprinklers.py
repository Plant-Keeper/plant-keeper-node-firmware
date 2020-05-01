"""

Plant keeper Sprinkler ESP32 firmware
Use:
    - Pin 34 for Capacitive soil moisture sensor
    - Pin 26 for sprinkler valve
    - TFT Screen ST7735 Pins: 12,13,14,16, 17, 18

Author : Shanmugathas Vigneswaran
mail : shangmuathas.vigneswaran@outlook.fr

"""
import gc
import time
from boot import SSID
from sysfont import sysfont
from ST7735 import TFT
from machine import SPI, Pin, ADC
from utils import fit
from pk import PlantKeeper
import node_type


NODE_TYPE = node_type.SPRINKLER
SPRINKLER_TAG = 'orchid'
PK_API_GATEWAY_HOST = '10.3.141.1'
PK_API_GATEWAY_PORT = 8001
POWER_COLOR = TFT.GREEN

SOIL_MOISTURE = ADC(Pin(34))
SOIL_MOISTURE.atten(ADC.ATTN_11DB)
SOIL_MOISTURE_FIT = fit(
    # MAP Analog read min/max
    [2300, 1110],
    # to 0% to 100%
    [0, 100]
)

RELAY = Pin(26, Pin.OUT)

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
tft.fillrect((0, 0), (128, 50), TFT.WHITE)
tft.fillrect((0, 50), (128, 160), TFT.RED)
tft.text((2, 2), "Wifi: " + SSID, TFT.BLACK, sysfont, 1.1, nowrap=False)
tft.text((2, 10), "Api Gateway:", TFT.BLACK, sysfont, 1.1, nowrap=False)
tft.text((2, 20), PK_API_GATEWAY_HOST + ":" + str(PK_API_GATEWAY_PORT), TFT.BLACK, sysfont, 1.1, nowrap=False)
tft.text((2, 30), "NodeType:", TFT.BLACK, sysfont, 1.1, nowrap=False)
tft.text((2, 40), NODE_TYPE, TFT.BLACK, sysfont, 1.1, nowrap=False)
tft.text((2, 50), "Tag: " + SPRINKLER_TAG, TFT.BLACK, sysfont, 1.1, nowrap=False)

pk = PlantKeeper(
    host=PK_API_GATEWAY_HOST,
    port=PK_API_GATEWAY_PORT
)
pk.set_node_type(node_type=NODE_TYPE)
last_power = False

if __name__ == '__main__':
    while True:
        try:
            sensor = SOIL_MOISTURE_FIT(SOIL_MOISTURE.read())
            pk.post({"soil_humidity": sensor, 'tag': SPRINKLER_TAG})

            if last_power:
                POWER_COLOR = TFT.GREEN
            else:
                POWER_COLOR = TFT.RED

            tft.fillrect((0, 50), (128, 160), POWER_COLOR)
            tft.text((2, 50), "Tag: " + SPRINKLER_TAG, TFT.BLACK, sysfont, 1.1, nowrap=False)
            tft.fillrect((95, 60), (30, 10), POWER_COLOR)
            tft.text((2, 60), "Soil humidity: " + str(sensor), TFT.BLACK, sysfont, 1.1, nowrap=False)
            tft.fillrect((40, 70), (30, 10), POWER_COLOR)
            tft.text((2, 70), "Power: " + str(pk.power), TFT.BLACK, sysfont, 1.1, nowrap=False)

            if not last_power:
                last_power = pk.power
                RELAY.value(pk.power)
            else:
                if pk.power != last_power:
                    RELAY.value(pk.power)

            last_power = pk.power
            gc.collect()
            time.sleep(0.5)

        except:
            last_power = 0
            tft.fillrect((95, 60), (30, 10), POWER_COLOR)
            tft.text((2, 60), "ERROR ", TFT.BLACK, sysfont, 2, nowrap=False)
            tft.text((2, 80), "POWER=0 ", TFT.BLACK, sysfont, 2, nowrap=False)
            tft.text(
                (2, 100),
                "Reason:  "
                " can not communicate with  API Gateway, "
                "is   the  server  up   and running ?",
                TFT.BLACK,
                sysfont,
                1.2,
                nowrap=False
            )
            time.sleep(2)
