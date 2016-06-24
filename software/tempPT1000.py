	 #!/usr/bin/python3

import os
import spidev
import time
spi = spidev.SpiDev()
spi.open(0, 0)

adc_0degrees = 213
adc_100degrees = 645

output = 255

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


while True:
	print(readTemp(2))
	time.sleep(0.9)
	setOutput()
