#!/usr/bin/python3

from w1thermsensor import W1ThermSensor
from time import *

while (True):
    for sensor in W1ThermSensor.get_available_sensors():
        print("Sensor %s hat die Temperatur %.2f" % (sensor.id, sensor.get_temperature()))
        sleep(1)