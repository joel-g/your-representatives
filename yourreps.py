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



# print(results.json()['resultsults'][0])
# print(results.json()['resultsults'][1])

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
    results = requests.get('https://whoismyrepresentative.com/getall_mems.php?zip=' + zip_code + '&output=json')
    if 'No Data Found' in results.text:
        return False
    else:
        return results.json()['results']

def reply_with_congressman(author, reps):
    # api.update_status(status= t.author.screen_name + "your congressman is " )
    print(
        "@" + author + " your rep in the house is:\n" + 
        reps[0]['name'] + "\n" + 
        "District: " + reps[0]['district'] + "\n" +
        "State: " + reps[0]['state'] + "\n" +
        "Party: " + reps[0]['party'] + "\n" + 
        "Phone: " + reps[0]['phone'] + "\n" +
        "Web: " + reps[0]['link']

    )


for m in mentions:
    zip_code = get_zip_code(m)
    # if is_replied_to(m):

    if not is_replied_to(m):
        if zip_code:
            reps = find_reps(zip_code)
            if reps:
                congressman = reps[0]
                senator1 = reps[1]
                senator2 = reps[2]
                reply_with_congressman(m.author.screen_name, reps)
                record_replied_to(m)

    print('---------')
        



