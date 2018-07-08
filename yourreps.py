import requests, sys, tweepy, re, time

config = open('config.ini','r')
tokens = config.readlines()
config.close()
replied_to = 'replied_to_log.txt'

CONSUMER_KEY = tokens[0].rstrip()
CONSUMER_SECRET = tokens[1].rstrip()
ACCESS_KEY = tokens[2].rstrip()
ACCESS_SECRET = tokens[3].rstrip()
TWITTER_ACCOUNTS = {'Ron Wyden': '@RonWyden', 'Gary Peters': ' @SenGaryPeters', 'Claire McCaskill': '@clairecmc', 'Dick Durbin': '@SenatorDurbin', 'Richard Blumenthal': '@SenBlumenthal', 'Richard Shelby': '@SenShelby', 'Marco Rubio': '@marcorubio', 'Debbie Stabenow': '@SenStabenow', 'Catherine Cortez Masto': '@SenCortezMasto', 'Ben Cardin': '@SenatorCardin', 'Saxby Chambliss': '@SaxbyChambliss', 'Cory Booker': '@CoryBooker', 'John Hoeven': '@SenJohnHoeven', 'Tom Carper': '@SenatorCarper', 'Tammy Baldwin': ' @SenatorBaldwin', 'Thad Cochran': '@SenThadCochran', 'Orrin Hatch': '@SenOrrinHatch', 'Sheldon Whitehouse': '@SenWhitehouse', 'Lisa Murkowski': '@lisamurkowski', 'Bob Menendez': '@SenatorMenendez', 'Angus King': ' @SenAngusKing', 'Maria Cantwell': '@SenatorCantwell', 'Jeff Merkley': '@SenJeffMerkley', 'Ron Johnson': '@SenRonJohnson', 'John Thune': '@SenJohnThune', 'Shelley Moore Capito': '@SenCapito', 'Jim Inhofe': '@jiminhofe', 'Patrick Leahy': '@SenatorLeahy', 'Jack Reed': '@SenJackReed', 'Jim Risch': '@SenatorRisch', 'Joe Donnelly': '@SenDonnelly ', 'Joni Ernst': '@joniernst', 'Dianne Feinstein': '@SenFeinstein', 'Chuck Grassley': '@ChuckGrassley', 'Mike Crapo': '@MikeCrapo', 'Deb Fischer': '@SenatorFischer', 'Mark Warner': '@MarkWarner', 'Martin Heinrich': '@MartinHeinrich', 'Kirsten Gillibrand': '@SenGillibrand', 'John Boozman': '@JohnBoozman', 'Mike Rounds': '@SenatorRounds', 'Chris Van Hollen': '@ChrisVanHollen', 'Ted Cruz': '@SenTedCruz', 'Tammy Duckworth': '@SenDuckworth', 'Bill Cassidy': '@BillCassidy', 'Pat Roberts': '@SenPatRoberts', 'Heidi Heitkamp': '@SenatorHeitkamp', 'Tom Udall': '@SenatorTomUdall', 'Bob Corker': '@SenBobCorker', 'Elizabeth Warren': '@SenWarren', 'Tim Kaine': '@timkaine', 'Cory Gardner': '@SenCoryGardner', 'Johnny Isakson': '@SenatorIsakson', 'Chuck Schumer': '@SenSchumer', 'Richard Burr': '@SenatorBurr', 'Maggie Hassan': '@GovernorHassan', 'Michael Bennet': '@SenBennetCO', 'Steve Daines': '@SteveDaines', 'Roger Wicker': '@SenatorWicker', 'Dan Sullivan': ' @SenDanSullivan', 'John McCain': '@SenJohnMcCain', 'John Barrasso': '@SenJohnBarrasso', 'Roy Blunt': '@RoyBlunt', 'John Neely Kennedy': '@SenJohnKennedy', 'Jeff Flake': '@JeffFlake', 'David Perdue': ' @SenDavidPerdue', 'Rand Paul': '@SenRandPaul', 'Bill Nelson': '@SenBillNelson', 'Mitch McConnell': ' @SenateMajLdr', 'Sherrod Brown': '@SenSherrodBrown', 'Ed Markey': '@senmarkey', 'Brian Schatz': '@brianschatz', 'John Cornyn': '@JohnCornyn', 'Mike Lee': '@SenMikeLee', 'Joe Manchin': '@Sen_JoeManchin', 'Christopher Murphy': '@ChrisMurphyCT', 'Kamala Harris': '@SenKamalaHarris', 'Patty Murray': '@PattyMurray', 'Luther Strange': '@lutherstrange', 'Bernie Sanders': '@SenatorSanders', 'Jeanne Shaheen': '@SenatorShaheen', 'Rob Portman': '@SenRobPortman', 'Thom Tillis': '@SenThomTillis', 'Dean Heller': '@SenDeanHeller', 'Lindsey Graham': '@GrahamBlog', 'Susan Collins': '@SenatorCollins', 'Chris Coons': '@ChrisCoons', 'Tom Cotton': '@SenTomCotton', 'Tim Scott': '@SenatorTimScott', 'Mike Enzi': '@SenatorEnzi', 'Lamar Alexander': '@SenAlexander', 'Todd Young': '@SenToddYoung', 'Ben Sasse': '@SenSasse', 'Mazie K. Hirono': '@maziehirono', 'Jerry Moran': '@JerryMoran', 'James Lankford': '@SenatorLankford', 'Amy Klobuchar': '@amyklobuchar', 'Patrick Toomey': '@SenToomey', 'Alan Franken': '@SenFranken', 'Robert Casey': '@SenBobCasey', 'Jon Tester': '@SenatorTester'}

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

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

def reply_with_reps(author, reps, tweet_id):
    for rep in reps:
        if rep['district']:
            try:
                api.update_status(
                "@" + author + "\n" +
                "Representative: " + rep['name'] + "\n" + 
                "District: " + rep['district'] + "\n" +
                "State: " + rep['state'] + "\n" +
                "Party: " + rep['party'] + "\n" + 
                "Phone: " + rep['phone'] + "\n" +
                "Web: " + rep['link'] + "\n"
                "Office: " + rep['office'],
                tweet_id
                )
                print("Replied with representative to " + author + "\n sleeping 30 seconds")
            except Exception as e:
                print("couldn't reply with representative " + rep['name'] + " to " + author)
                print(e)
        else:
            try:
                twitter_account = TWITTER_ACCOUNTS[rep['name']]
            except:
                twitter_account = ''
                print('Couldn\'t assign twitter handle for: ' + rep['name'])
            try:
                api.update_status(
                "@" + author + "\n" +
                "Senator: " + rep['name'] + " " + twitter_account + "\n" + 
                "State: " + rep['state'] + "\n" +
                "Party: " + rep['party'] + "\n" + 
                "Phone: " + rep['phone'] + "\n" +
                "Web: " + rep['link'] + "\n"
                "Office: " + rep['office'],
                tweet_id
                )
                print("Replied with senator " + rep['name'] + " to " + author + "\n sleeping 30 seconds")
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
                reply_with_reps(m.author.screen_name, reps, m.id)
                record_replied_to(m)
        print('---------')
        
while True:
    print('Starting...')
    rep_engine()
    print('Waiting 5 minutes')
    time.sleep(300)

