 #!/usr/bin/python3

import os
import spidev
import time
import json
import configparser
from urllib.request import urlopen

config = configparser.ConfigParser()
try:
	config.read('/home/pi/Documents/config.txt')
except:
	print("configuration-file not found!\n")

adc_0degrees = 213
adc_100degrees = 645


class CtrlHardware():
	_output = 0xff
	spi = spidev.SpiDev()
	spi.open(0, 0)

	#sensor_id: 0..15
	def readTemp (self, sensor_id):
		if sensor_id >= 0 and sensor_id < 8:
			#set output-latch of GPB3 low, GPB4 high
			mux_byte = format(16+sensor_id, '#04x')
			os.system('i2cset -y 1 0x24 0x15 '+mux_byte)
		elif sensor_id >7 and sensor_id < 16:
			#set output-latch of GPB3 high, GPB4 low
			mux_byte = format(sensor_id, '#04x')
			os.system('i2cset -y 1 0x24 0x15 '+mux_byte)
		#set pins 0..4 of register B as output
		os.system('i2cset -y 1 0x24 0x01 0xE0')
		time.sleep (0.1)
		adc_result = self.spi.xfer([0x01, 0x80, 0x00])
		value = 256*adc_result[1] + adc_result[2]
		Temp = 100.0*(value - adc_0degrees)/(adc_100degrees - adc_0degrees)
		return Temp

	def initOutputs (self):
		self._output = 0xff
		os.system('i2cset -y 1 0x20 0x15 0xFF')
		os.system('i2cset -y 1 0x20 0x01 0x00')  # set pins 0..7 of register B as output

	def setOutput (self, output):
		self._output = (~output + 256)
		os.system('i2cset -y 1 0x20 0x15 ' + format(self._output, '#04x'))
		os.system('i2cset -y 1 0x20 0x01 0x00')  #set pins 0..4 of register B as output

	def changeOutput (self, pin=0, state=0):
		if (state == 0):
			self._output = self._output | (2**pin)
		else:
			self._output = self._output & ((~(2**pin))+ 256)
		os.system('i2cset -y 1 0x20 0x15 ' + format(self._output, '#04x'))
		os.system('i2cset -y 1 0x20 0x01 0x00')  #set pins 0..4 of register B as output

	def postData (self, data, node):
		rw_apikey = config['local_emon']['rw_apikey']
		url = 'http://localhost/emoncms/input/post.json?node='+str(1)+'&json={'+data+'}&apikey='+rw_apikey
		answer = urlopen(url)
		#print(answer)

	def postDataRemoteServer (self, data, node):
		url = 'xxxxxxxxxxxxxxx/emoncms/input/post.json?node='+str(1)+'&json={'+data+'}&apikey=xxxxxxxxxxxxxx'
		answer = urlopen(url)
		#print(answer)

	def setRelais0 (self):
		#os.system('i2cset -y 1 0x24 0x15 0x10')  #set output-latch of GPB4 high
		#os.system('i2cset -y 1 0x24 0x01 0xE0')  #set pins 0..4 of register B as output
		os.system('i2cset -y 1 0x20 0x15 0xFE')
		os.system('i2cset -y 1 0x20 0x01 0x00')  #set pins 0..7 of register B as output

	def resetRelais0 (self):
		os.system('i2cset -y 1 0x20 0x15 0xFF')
		os.system('i2cset -y 1 0x20 0x01 0x00')  #set pins 0..7 of register B as output


	
