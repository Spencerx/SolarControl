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

SolarPumpRunning = False
SwitchOnTime = 0

spi = spidev.SpiDev()
spi.open(0, 0)

adc_0degrees = 213
adc_100degrees = 645

#sensor_id: 0..15
def readTemp (sensor_id):   
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
	adc_result = spi.xfer([0x01, 0x80, 0x00])
	value = 256*adc_result[1] + adc_result[2]
	Temp = 100.0*(value - adc_0degrees)/(adc_100degrees - adc_0degrees)
	return Temp

def setOutput (pin=0, state=0):
	os.system('i2cset -y 1 0x20 0x15 ' + format(output, '#04x'))  
	os.system('i2cset -y 1 0x20 0x01 0x00')  #set pins 0..4 of register B as output


def postData (data, node):
	rw_apikey = config['local_emon']['rw_apikey']
	url = 'http://localhost/emoncms/input/post.json?node='+str(1)+'&json={'+data+'}&apikey='+rw_apikey
	answer = urlopen(url)
	#print(answer)

def postDataRemoteServer (data, node):
	url = 'xxxxxxxxxxxxxxx/emoncms/input/post.json?node='+str(1)+'&json={'+data+'}&apikey=xxxxxxxxxxxxxx'
	answer = urlopen(url)
	#print(answer)


def setRelais0 ():
	#os.system('i2cset -y 1 0x24 0x15 0x10')  #set output-latch of GPB4 high
	#os.system('i2cset -y 1 0x24 0x01 0xE0')  #set pins 0..4 of register B as output
	os.system('i2cset -y 1 0x20 0x15 0xFE')  
	os.system('i2cset -y 1 0x20 0x01 0x00')  #set pins 0..7 of register B as output

def resetRelais0 ():
	os.system('i2cset -y 1 0x20 0x15 0xFF')  
	os.system('i2cset -y 1 0x20 0x01 0x00')  #set pins 0..7 of register B as output


#########################

Relais = 0
resetRelais0 ()

while True:
	T1 = readTemp(0)
	T2 = readTemp(1)
	T3 = readTemp(2)
	T4 = readTemp(3)
	T5 = readTemp(4)
	T6 = readTemp(5)
	T7 = readTemp(6)
	T8 = readTemp(7)
	T9 = readTemp(8)
	T10 = readTemp(9)
	T11 = readTemp(10)
	
	TempLog = "T1:%2.1f,T2:%2.1f,T3:%2.1f,T4:%2.1f,T5:%2.1f,T6:%2.1f,T7:%2.1f,T8:%2.1f,T9:%2.1f,T10:%2.1f,T11:%2.1f" % (T1, T2, T3, T4, T5, T6, T7, T8, T9, T10, T11)
	print ("T1 = %2.1f, T2 = %2.1f, T3 = %2.1f, T4 = %2.1f, T5 = %2.1f, T6 = %2.1f, T7 = %2.1f" % (T1, T2, T3, T4, T5, T6, T7))
	print("T8 = %2.1f, T9 = %2.1f, T10 = %2.1f, T11 = %2.1f" % (T8, T9, T10, T11))
	postData(TempLog, 1)
	#postDataRemoteServer(TempLog,27)


	#mean-temperature:
	StorageMeanTemp = (T1*30 + T2*5 + T3*5 + T4*10 + T5*20 + T6*30)/100

	if (StorageMeanTemp>81):  #activ cooling
		SolarPumpRunning = True
		setRelais0()
		SwitchOnTime = 0
	else:
		if SolarPumpRunning:
			SwitchOnTime += 30
			if (T9>T8)and(SwitchOnTime>300):
				SolarPumpRunning = False
				resetRelais0()
				SwitchOnTime = 0
		elif (T7 > (T6 + 4)):
			SolarPumpRunning = True
			setRelais0()

	time.sleep (30)
	
