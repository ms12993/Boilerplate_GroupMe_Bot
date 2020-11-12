# RESOURCE: http://www.apnorton.com/blog/2017/02/28/How-I-wrote-a-Groupme-Chatbot-in-24-hours/


# IMPORTS
import os
import json
import requests
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request
import re
import random
import datetime

app = Flask(__name__)
bot_id = os.getenv('GROUPME_BOT_ID')

# get list of groups
url = 'https://api.groupme.com/v3/groups/12804350?token='#56351881?token='
token = 'Mq0l3yrFmlJ6n7Gc1wopPT00Hn2GEQWAZlkejpvP'
url = url + token

response = requests.get(url)
data = json.loads(response.text)
data = data['response']

members = {}
for i in range(len(data['members'])):
	members[data['members'][i]['user_id']] = {}
	members[data['members'][i]['user_id']]['name'] = data['members'][i]['nickname'] 

# lcr = {
#     'Players': {   
#     },
#     'Center':0,
#     'Over':1   
# }

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['POST'])
def webhook():
	# 'message' is an object that represents a single GroupMe message.
	message = request.get_json()
	try:
		tagged = message['attachments'][0]['user_ids']
		#tagged.append(message['sender_id'])
	except:
		tagged = []
	#if 1+1 == 2 and not sender_is_bot(message):
		#reply(message)
		
	if '5:38' in message['text'].lower() and not sender_is_bot(message) or '538' in message['text'].lower() and not sender_is_bot(message):
		dt = datetime.datetime.now(tz=EST5EDT())
		sdt = dt.strftime('%H:%M')
		if sdt == '17:38':
			url = random_gif('')
			reply_with_image('haaaaaaaan',url)
		if sdt == '18:38':
			url = random_gif('')
			reply_with_image('haaaaaaaan.....EST',url)
		if sdt != '17:38' and sdt != '18:38' and std != '05:38':
			reply('Nice try you fucking dumbass')
		
		if sdt == '05:38' or sdt == '06:38':
			reply('go back to fucking bed')
			
	if message['text'][:8] == '!masters': 
		if 'leaderboard' in message['text'].lower():
			table = get_leaders()
			reply(table)

	if message['text'][:5] == '!ogre': 
		
		if 'wz' in message['text'].lower() and not sender_is_bot(message): # if message contains 'groot', ignoring case, and sender is not a bot...
			try:
				people = re.findall('layers:(.*?);',message['text'])[0].strip()
				people = Convert(people)
				nTeams = int(re.findall('eams:(.*?)$',message['text'])[0].strip())
				teams = partition(people,nTeams)
				mes = ''
				idx = 1
				for team in teams:
					if idx == 1:
						mes += 'Team ' + str(idx) + ':\n' + ', '.join(team)
					else:
						mes += '\nTeam ' + str(idx) + ':\n' + ', '.join(team)
					idx += 1
				mes += '\nGL;HF! See you back in 3 games'
				reply(mes)
			except:
				reply('please follow the correct format. use !ogre help for more info.\n Dumbass :)')

		if 'groot' in message['text'].lower() and not sender_is_bot(message): # if message contains 'groot', ignoring case, and sender is not a bot...
			reply('I am Groot.')
			
		if 'poker' in message['text'].lower() and not sender_is_bot(message):
			pokerMes = '7pm - 4/20\nMeeting ID: 974-6496-7510\nPassword: 538538\nBuy in/Buy Back: $20\nJust log into the fucking zoom call :))))'
			reply(pokerMes)

		if 'weather' in message['text'].lower() and not sender_is_bot(message):
			try:
				city = re.findall(':(.*?)$',message['text'])[0].strip()
				getWeather(city)
			except:
				#city = 'na'
				reply('Cannot Find a city in your message. Please try again in the format "Weather: City" \n Dumbass :)')
	
		if 'coin' in message['text'].lower() and not sender_is_bot(message):
			coin()
	
		if 'gif' in message['text'].lower() and not sender_is_bot(message):
			try:
				searchTerm = re.findall('gif:(.*?)$',message['text'])[0].strip()
				searchTerm = str(searchTerm)
				url = random_gif(searchTerm,rand=False)
				reply_with_image(searchTerm,url)
			except:
				reply('please follow the correct format. use !ogre help for more info.\n Dumbass :)')
		if '8ball' in message['text'].lower() and not sender_is_bot(message):
			eightBall()
			
		if 'help' in message['text'].lower() and not sender_is_bot(message):
			reply('Here is a list of my commands: \n!ogre coin - flips a coin\n!ogre weather: city - returns weather\n!ogre 8ball\n!ogre WZ: players:comma seperated players ; teams: number of teams\nFor more functions, please venmo Matt-Sarver with request attached')
			
		if 'lcr/roll' in message['text'].lower() and not sender_is_bot(message):
			lcr = json.loads(os.getenv('lcr'))
			if lcr['Over'] == 0:
				userId, name = turn(lcr)
				if str(message['sender_id']) == userId:
					pos = position(lcr, str(message['sender_id']))
					die = roll(lcr['Players'][pos]['chips'])
					message = die + '\n'
					lcr, ret = distribute(lcr, die, pos)
					score = scoreboard(lcr)
					message += score + '\n'
					#print(score)
					message += ret + '\n'
					reply(message)
					lcr, over = gameOver(lcr)
					if len(over) > 0:
						reply(over)
				else:
					reply('not your turn. ' + name + ' is up!')
			else:
				reply('no current game active. please use new game command')
				
		if 'lcr/new game' in message['text'].lower() and not sender_is_bot(message):
			lcr, message = newGame(tagged)
			reply(message)
        
	if len(tagged) > 0:
		if '13831863' in tagged: # steve- 13831863 sean- 12377981
			reply('Thanks for reaching out to Stephanie. Please expect a reply in 12-72 hours (maybe).')
	if message['system'] == True:
		if 'added' in message['text'].lower():
			name = re.findall('added (.*?) to the',message['text'])[0].strip()
			print(name)
			string = 'Welcome to the group, ' + name + ' please tread lightly'
			reply(string)
		if 'removed' in message['text'].lower():
			name = re.findall('removed (.*?) from the',message['text'])[0].strip()
			string = 'lol get rekt, ' + name + '!'
			print(string)
			reply(string)
	return "ok", 200

################################################################################

# Send a message in the groupchat
def reply(msg):
	url = 'https://api.groupme.com/v3/bots/post'
	data = {
		'bot_id'		: bot_id,
		'text'			: msg
	}
	request = Request(url, urlencode(data).encode())
	print(url, data)
	json = urlopen(request).read().decode()

# Send a message with an image attached in the groupchat
def reply_with_image(msg, imgURL):
	url = 'https://api.groupme.com/v3/bots/post'
	urlOnGroupMeService = upload_image_to_groupme(imgURL)
	data = {
		'bot_id'		: bot_id,
		'text'			: msg,
		'picture_url'		: urlOnGroupMeService
	}
	request = Request(url, urlencode(data).encode())
	json = urlopen(request).read().decode()
	
# Uploads image to GroupMe's services and returns the new URL
def upload_image_to_groupme(imgURL):
	imgRequest = requests.get(imgURL, stream=True)
	filename = 'temp.png'
	postImage = None
	if imgRequest.status_code == 200:
		# Save Image
		with open(filename, 'wb') as image:
			for chunk in imgRequest:
				image.write(chunk)
		# Send Image
		headers = {'content-type': 'application/json'}
		url = 'https://image.groupme.com/pictures'
		files = {'file': open(filename, 'rb')}
		payload = {'access_token': 'Mq0l3yrFmlJ6n7Gc1wopPT00Hn2GEQWAZlkejpvP'}
		r = requests.post(url, files=files, params=payload)
		imageurl = r.json()['payload']['url']
		os.remove(filename)
		return imageurl
	
	
def get_leaders():
    response = requests.get('https://www.espn.com/golf/leaderboard')
    df = pd.read_html(response.text)[0].head()
    
    return df.to_string()

	
def getWeather(city):
    api_key = "cfeaa4d330ea4fed547004a561111a2e"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    city_name = city
    complete_url = base_url + "appid=" + api_key + "&q=" + city_name 
    response = requests.get(complete_url) 
    x = response.json() 

    if x["cod"] != "404": 
        y = x["main"] 
        current_temperature = y["temp"]
        current_temperature = (int(current_temperature) - 273.15) * 9/5 + 32
        current_pressure = y["pressure"] 
        current_humidiy = y["humidity"] 
        z = x["weather"] 
        weather_description = z[0]["description"] 
        # print following values 
        reply("Temperature: " +
                        str(round(current_temperature,2)) + 
              "\nHumidity: " +
                        str(current_humidiy) +
              "\nDescription: " +
                        str(weather_description)) 
        #reply(msg)
  
    else: 
        reply(" City Not Found ")

	
def coin():
    flip = random.randint(0,1)
    if flip == 0:
        coin = 'Heads'
    else:
        coin = 'Tails'
    reply(coin)

def eightBall():
    eightBall = random.randint(1,9)
    if eightBall == 1:
        answer = "It is certain"
    
    elif eightBall == 2:
        answer = "Outlook good"
    
    elif eightBall == 3:
        answer = "You may rely on it"
    
    elif eightBall == 4:
        answer = "Ask again later"
    
    elif eightBall == 5:
        answer = "Concentrate and ask again"
    
    elif eightBall == 6:
        answer = "Reply hazy, try again"
    
    elif eightBall == 7:
        answer = "My reply is no"
    
    elif eightBall == 8:
        answer = "My sources say no"
        
    elif eightBall == 9:
        answer = "Steve Smells"
        
    reply(answer)

def newGame(tagged):
	url = 'https://api.groupme.com/v3/groups/12804350?token='#56351881?token='
	token = 'Mq0l3yrFmlJ6n7Gc1wopPT00Hn2GEQWAZlkejpvP'
	url = url + token

	response = requests.get(url)
	data = json.loads(response.text)
	data = data['response']

	for i in range(len(data['members'])):
		members[data['members'][i]['user_id']] = {}
		members[data['members'][i]['user_id']]['name'] = data['members'][i]['nickname'] 
	pos = 0
	lcr = {
	    'Players': {   
	    },
	    'Center':0,
	    'Over':1   
	}

	string = ''
	for i in range(len(tagged)):
		lcr['Players'][i] = {}
		lcr['Players'][i]['userId'] = tagged[i]
		lcr['Players'][i]['position'] = pos
		lcr['Players'][i]['chips'] = 3
		lcr['Players'][i]['turn'] = 0
		lcr['Players'][i]['name'] = members[str(tagged[i])]['name']
		pos += 1
	lcr['Players'][0]['turn'] = 1
	lcr['Center'] = 0
	lcr['Over'] = 0
	string = 'New game has been started with ' + str(len(tagged)) + ' people ' + members[str(tagged[0])]['name'] + ' is up first!'
	os.environ["lcr"] = json.dumps(lcr)
	return lcr, string

def roll(num):
    dice = ['-','-','-','Left','Center','Right']
    if num > 3:
        num = 3
    die = []
    for i in range(0,num):
        die.append(random.choice(dice))
    return die

def distribute(lcr, die, pos):
    message = ''
    for i in range(len(die)):
        if die[i] == 'Right':
            lcr['Players'][pos]['chips'] -= 1
            try:
                lcr['Players'][pos + 1]['chips'] += 1
                #message += lcr['Players'][pos + 1]['name'] + ' + 1: ' + str(lcr['Players'][pos + 1]['chips']) + '\n'
            except:
                lcr['Players'][0]['chips'] += 1
                #message += lcr['Players'][0]['name'] + ' + 1: ' + str(lcr['Players'][0]['chips']) + '\n'

        if die[i] == 'Left':
            lcr['Players'][pos]['chips'] -= 1
            try:
                lcr['Players'][pos - 1]['chips'] += 1
                #message += lcr['Players'][pos - 1]['name'] + ' + 1: ' + str(lcr['Players'][pos - 1]['chips']) + '\n'
            except:
                lcr['Players'][len(lcr['Players'])-1]['chips'] += 1
                #message += lcr['Players'][len(lcr['Players'])-1]['name'] + ' + 1: ' + str(lcr['Players'][len(lcr['Players'])-1]['chips']) + '\n'

        if die[i] == 'Center':
            lcr['Players'][pos]['chips'] -= 1
            lcr['Center'] += 1
            #message += 'Center + 1: ' + str(lcr['Center']) + '\n'
    
    
    lcr['Players'][pos]['turn'] = 0
    nextUp = playerUp(lcr, lcr['Players'], pos)
    message += nextUp + ' is now up!'
    return lcr, message

def starting_with(arr, start_index):
     # use xrange instead of range in python 2
    for i in range(start_index, len(arr)):
        yield arr[i]
    for i in range(start_index):
        yield arr[i]

def playerUp(lcr, list, pos):
    player = ''
    for value in starting_with(list, pos + 1):
        if player == '':
            if value['chips'] > 0:
                player = value['name']
                value['turn'] = 1
                
    return player

def scoreboard(lcr):
    score = ''
    for i in range(len(lcr['Players'])):
        score += lcr['Players'][i]['name'] + ': ' + str(lcr['Players'][i]['chips']) + '\n'
    return score

def gameOver(lcr):
    players = []
    for x in lcr['Players']:
        if lcr['Players'][x]['chips'] != 0:
            players.append(lcr['Players'][x]['name'])
    if len(players) == 1:
        #print(str(players[0]) + ' has won the game!')
        lcr['Over'] = 1
        message = 'Game Over. ' + str(players[0]) + ' has won the game!'
    else:
        message = ''
    return lcr, message

def turn(lcr):
    for i in range(len(lcr['Players'])):
        if lcr['Players'][i]['turn'] == 1:
            
            return lcr['Players'][i]['userId'], lcr['Players'][i]['name']
	
def position(lcr, sender_id):
    pos = 0
    for i in range(len(lcr['Players'])):
        if sender_id == lcr['Players'][i]['userId']:
            pos = i
    return pos

def Convert(string):
	li = list(string.split(","))
	return li

def partition(list_in,n):
	random.shuffle(list_in)
	return [list_in[i::n] for i in range(n)]

class EST5EDT(datetime.tzinfo):

    def utcoffset(self, dt):
        return datetime.timedelta(hours=-5) + self.dst(dt)

    def dst(self, dt):
        d = datetime.datetime(dt.year, 3, 8)        #2nd Sunday in March
        self.dston = d + datetime.timedelta(days=6-d.weekday())
        d = datetime.datetime(dt.year, 11, 1)       #1st Sunday in Nov
        self.dstoff = d + datetime.timedelta(days=6-d.weekday())
        if self.dston <= dt.replace(tzinfo=None) < self.dstoff:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(0)

    def tzname(self, dt):
        return 'EST5EDT'

adjectives = ['cupid shuffle',
 'drunk',
 'lively',
 'creep',
 'sexy',
 'creepy',
 'macho',
 'pizza',
 'doggo',
 'weak',
 '50 shades',
 'grey',
 'tease',
 'accidental',
 'rampant',
 'souja boy',
 'lil wayne',
 'chance the rapper',
 'k',
 'line dance',
 'cocaine',
 'meth',
 'heroin',
 'marijuana',
 'weed',
 'handy',
 'ripe',
 'embarrassed',
 'alcohol',
 'party',
 'watch me whip',
 'boobs',
 'fortnite',
 'naughty',
 'exclusive',
 'lyrical',
 'sesame street',
 'disturbed',
 'gangster',
 'bobby shmruda',
 'repulsive',
 'chief keef',
 'lean',
 'dance',
 'sex',
 'ruthless',
 'cupid shuffle',
 'ugly',
 'drunk dance',
 'rave']

def random_gif(searchTerm='',rand=True):
	if rand==True:
		search = random.choice(adjectives)
	else:
		search = searchTerm
	url = 'https://api.giphy.com/v1/gifs/search?'
	api_key = 'SdSVKWszL9vaAPOh6O98uiSgxoNFm9yL'
	url += '&api_key=' + api_key
	query = search.replace(' ','+')
	url += '&q=' + query
	limit = 10
	url += '&limit=' + str(limit)

	response = requests.get(url)
	data = json.loads(response.text)
	data = data['data']
	num = random.randint(0,9)
	url = data[num]['images']['downsized_large']['url']
	
	return url
# Checks whether the message sender is a bot
def sender_is_bot(message):
	return message['sender_type'] == "bot"
