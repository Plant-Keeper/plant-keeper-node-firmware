Prepare ESP32 + MicroPython
===========================

Flash ESP

.. code-block:: shell

    pipenv install
    pipenv shell
    # for windows machine
    make flash-mp -e PORT=COM3
    # for Linux/macOS it will be something like that
    # example for Silicon Lab UART<>USB chip
    make flash-mp -e PORT=/dev/tty.SLAB_USBtoUART

Use Makefile to change Micropython firmware link to latest

Write Sprinkler firmware
========================

- Change settings.py: WIFI_SSID, WIFI_PASSWORD, MQTT_SERVER (and MQTT_PORT if needed)
- Change in main_sprinklers_mqtt.py **NODE_TAG** with a unique name describing the sprinkler
- Run this command to minify and write python file to ESP32

.. code-block:: shell

    put-sprinkler-firmware -e PORT=COM3
    # or for Linux/macOS
    put-sprinkler-firmware -e PORT=/dev/tty.SLAB_USBtoUART
