import requests, sys, tweepy

config = open('config.ini','r')
tokens = config.readlines()
config.close()

consumer_key = tokens[0]
consumer_secret = tokens[1]
access_key = tokens[2]
access_secret = tokens[3]


print(access_key)


res = requests.get('https://whoismyrepresentative.com/getall_mems.php?zip=98404&output=json')

# print(res.json()['results'][0])
# print(res.json()['results'][1])

