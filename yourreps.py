import requests, sys, tweepy, re, time

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
        f.write(str(tweet.id) + '\n')

def find_reps(zip_code):
    results = requests.get('https://whoismyrepresentative.com/getall_mems.php?zip=' + zip_code + '&output=json')
    if 'No Data Found' in results.text:
        return False
    else:
        return results.json()['results']

def reply_with_reps(author, reps):
    for rep in reps:
        if rep['district']:
            try:
                api.update_status(status=
                "@" + author + "\n" +
                "Representative: " + rep['name'] + "\n" + 
                "District: " + rep['district'] + "\n" +
                "State: " + rep['state'] + "\n" +
                "Party: " + rep['party'] + "\n" + 
                "Phone: " + rep['phone'] + "\n" +
                "Web: " + rep['link'] + "\n"
                "Office: " + rep['office']
                )
                print("Replied with representative to " + author + "\n sleeping 30 seconds")
            except Exception as e:
                print("couldn't reply with representative " + rep['name'] + " to " + author)
                print(e)
        else:
            try:
                api.update_status(status=
                "@" + author + "\n" +
                "Senator: " + rep['name'] + "\n" + 
                "State: " + rep['state'] + "\n" +
                "Party: " + rep['party'] + "\n" + 
                "Phone: " + rep['phone'] + "\n" +
                "Web: " + rep['link'] + "\n"
                "Office: " + rep['office']
                )
                print("Replied with senator to " + author + "\n sleeping 30 seconds")
            except Exception as e:
                print("couldn't reply with senator " + rep['name'] + " to " + author)
                print(e)
        time.sleep(30)

def rep_engine():
    mentions = api.mentions_timeline()
    for m in mentions:
        zip_code = get_zip_code(m)
        if zip_code and not is_replied_to(m):
            reps = find_reps(zip_code)
            if reps:
                reply_with_reps(m.author.screen_name, reps)
                record_replied_to(m)
        print('---------')
        
while True:
    print('Starting...')
    rep_engine()
    print('Waiting 10 minutes')
    time.sleep(600)


