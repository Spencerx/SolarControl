#!/usr/bin/python3

from w1thermsensor import W1ThermSensor
from time import *
import configparser
from urllib.request import urlopen

config = configparser.ConfigParser()
try:
	config.read('/home/pi/Documents/config.txt')
except:
	print("configuration-file not found!\n")


def postData(data, node):
    rw_apikey = config['local_emon']['rw_apikey']
    url = 'http://localhost/emoncms/input/post.json?node=' + str(node) + '&json={' + data + '}&apikey='+rw_apikey
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