 #!/usr/bin/python3

import configparser
from urllib.request import urlopen

config = configparser.ConfigParser()
try:
	config.read('/home/pi/Documents/config.txt')
except:
	print("configuration-file not found!\n")


class EnergyMonitor():
	def postData (self, data, node):
		rw_apikey = config['local_emon']['rw_apikey']
		url = 'http://localhost/emoncms/input/post.json?node='+str(1)+'&json={'+data+'}&apikey='+rw_apikey
		answer = urlopen(url)
		#print(answer)

	def readHeatingTempSetpoint (self):
		#rw_apikey = config['local_emon']['rw_apikey']
		url = 'http://192.168.1.107/emoncms/feed/value.json?id=14&apikey=' + rw_apikey

		try:
			sock = urlopen(url)
			data_str = sock.read()
			sock.close
		except:
			print ("Error in reading emoncms data")
			data_str = '0'

		return float((data_str.decode("utf-8")).replace('"', ''))

	def postDataRemoteServer (self, data, node):
		url = 'xxxxxxxxxxxxxxx/emoncms/input/post.json?node='+str(1)+'&json={'+data+'}&apikey=xxxxxxxxxxxxxx'
		answer = urlopen(url)
		#print(answer)



	
