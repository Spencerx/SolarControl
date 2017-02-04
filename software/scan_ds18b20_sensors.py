#!/usr/bin/python3

from w1thermsensor import W1ThermSensor
from time import *


def postData(data, node):
    url = 'http://localhost/emoncms/input/post.json?node=' + str(node) + '&json={' + data + '}
    answer = urlopen(url)

Sensors = W1ThermSensor.get_available_sensors()


while (True):
    for sensor in Sensors:
        id = sensor.id
        temp = sensor.get_temperature()
        print("Sensor %s hat die Temperatur %.2f" % (id, temp))
        SensorData = "%s:%.2f" % (id, temp)
        try:
            postData(SensorData, 1)
        except:
            print("posting data not successful\n")
        sleep(1)