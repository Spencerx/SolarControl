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
		rw_apikey = config['local_emon']['rw_apikey']
		url = 'http://localhost/emoncms/feed/value.json?id=14&apikey=' + rw_apikey
		try:
			sock = urlopen(url)
			data_str = sock.read()
			sock.close
			return float((data_str.decode("utf-8")).replace('"', ''))
		except:
			return 0.0

	def postDataRemoteServer (self, data, node):
		url = 'xxxxxxxxxxxxxxx/emoncms/input/post.json?node='+str(1)+'&json={'+data+'}&apikey=xxxxxxxxxxxxxx'
		answer = urlopen(url)
		#print(answer)



	
