Plant Keeper Client for ESP32
=============================


Quick start
===========

Usage for sprinkler

.. code-block:: shell

    from machine import Pin, ADC
    from pk_node_core.pk import Client
    from pk_node_core import node_type

    SOIL_SENSOR_TAG = 'plant-1'

    soil_humidity_sensor = ADC(Pin(34))
    soil_humidity_sensor.atten(ADC.ATTN_11DB) # full range voltage: 3.3V

    client = Client(host='192.168.0.21', port=8001)
    client.set_node_type(node_type.SPRINKLER)

    sensor_humidity = soil_humidity_sensor.read()

    while True:
        client.post(
            dict(
                tag=SOIL_SENSOR_TAG,
                soil_humidity=sensor_humidity
                )
        )

        if client.power == True:
            activate_valve = True
        else:
            activate_valve = False
