import requests, sys, tweepy, re

config = open('config.ini','r')
tokens = config.readlines()
config.close()
replied_to = 'replied_to_log.txt'

CONSUMER_KEY = tokens[0].rstrip()
CONSUMER_SECRET = tokens[1].rstrip()
ACCESS_KEY = tokens[2].rstrip()
ACCESS_SECRET = tokens[3].rstrip()

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)



# print(res.json()['results'][0])
# print(res.json()['results'][1])

# api.update_status(status="test")
mentions = api.mentions_timeline()

def get_zip_code(tweet):
    if re.search('\d{5}', tweet.text):
        return re.search('\d{5}', tweet.text).group(0)
    else:
        return None

def is_replied_to(tweet):
     with open(replied_to, 'r') as f:
        if str(tweet.id) in f.read():
            return True
        else:
            return False

def record_replied_to(tweet):
    with open(replied_to, 'a') as f:
        f.write(str(m.id) + '\n')

def find_reps(zip_code):
    res = requests.get('https://whoismyrepresentative.com/getall_mems.php?zip=' + zip_code + '&output=json')
    print(res.json())    

for m in mentions:
    zip_code = get_zip_code(m)
    # if is_replied_to(m):

    if not is_replied_to(m):
        record_replied_to(m)
    print(zip_code)
    print((m.author.screen_name))
    print(m.text)
    print(m.id)
    print('---------')
        
find_reps('98404')


