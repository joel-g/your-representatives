import requests
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('config.ini')

res = requests.get('https://whoismyrepresentative.com/getall_mems.php?zip=98404&output=json')

print(res.json()['results'][0])
print(res.json()['results'][1])