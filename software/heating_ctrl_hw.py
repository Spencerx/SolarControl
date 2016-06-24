 #!/usr/bin/python3

import os
import spidev
import time
import json
from urllib.request import urlopen

spi = spidev.SpiDev()
spi.open(0, 0)

os.system('i2cset -y 1 0x24 0x15 0x10')  #set output-latch of GPB4 high
os.system('i2cset -y 1 0x24 0x01 0xE0')  #set pins 0..4 of register B as output

output = 0

#os.system('i2cset -y 1 0x20 0x15 0xF9')  
#os.system('i2cset -y 1 0x20 0x01 0x00')  #set pins 0..7 of register B as output

while True:
	adc_result = spi.xfer([0x01, 0x80, 0x00])
	value = 256*adc_result[1] + adc_result[2]
	print(value)
	#relais: set output-latch of GPBx
	os.system('i2cset -y 1 0x20 0x15 ' + format(output, '#04x'))  
	os.system('i2cset -y 1 0x20 0x01 0x00')  #set pins 0..4 of register B as output
	print(format(output, '#04x'))
	if output < 7:
		output = output+1
	else:
		output = 0
	url = 'http://localhost/emoncms/input/post.json?node=1&json={power:'+str(output)+'}&apikey=e5703b02d65a9a05315eee981682f1d1'
	answer = urlopen(url)
	print(answer)
	time.sleep(5)
