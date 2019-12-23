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

app = Flask(__name__)
bot_id = os.getenv('GROUPME_BOT_ID')

lcr = {
    'Players': {   
    },
    'Center':0,
    'Over':1   
}

# Called whenever the app's callback URL receives a POST request
# That'll happen every time a message is sent in the group
@app.route('/', methods=['POST'])
def webhook():
	# 'message' is an object that represents a single GroupMe message.
	message = request.get_json()
	try:
		tagged = message['attachments'][0]['user_ids']
	except:
		tagged = []
	#if 1+1 == 2 and not sender_is_bot(message):
		#reply(message)
		
	#if 'ogre' in message['text'].lower() and not sender_is_bot(message):
		#reply('GET OUT ME SWAMP')
	
	if message['text'][:5] == '!ogre': 

		if 'groot' in message['text'].lower() and not sender_is_bot(message): # if message contains 'groot', ignoring case, and sender is not a bot...
			reply('I am Groot.')

		if 'weather' in message['text'].lower() and not sender_is_bot(message):
			try:
				city = re.findall(':(.*?)$',message['text'])[0].strip()
				getWeather(city)
			except:
				#city = 'na'
				reply('Cannot Find a city in your message. Please try again in the format "Weather: City" \n Dumbass :)')
	
		if 'coin' in message['text'].lower() and not sender_is_bot(message):
			coin()
	
		if '8ball' in message['text'].lower() and not sender_is_bot(message):
			eightBall()
			
		if 'help' in message['text'].lower() and not sender_is_bot(message):
			reply('Here is a list of my commands: \n!ogre coin - flips a coin\n!ogre weather: city - returns weather\n!ogre 8ball\nFor more functions, please venmo Matt-Sarver with request attached')
			
		if 'lcr/roll' in message['text'].lower() and not sender_is_bot(message):
			if lcr['Over'] == 0:
				userId, name = turn()
				if str(message['sender_id']) == userId:
					pos = position(str(message['sender_id']))
					die = roll(lcr['Players'][pos]['chips'])
					message = die + '\n'
					ret = distribute(die, pos)
					score = scoreboard()
					message += score + '\n'
					#print(score)
					message += ret + '\n'
					reply(message)
					over = gameOver()
					if len(over) > 0:
						reply(over)
				else:
					reply('not your turn. ' + name + ' is up!')
			else:
				reply('no current game active. please use new game command')
        
	if len(tagged) > 0:
		if '13831863' in tagged:
			reply('Thanks for reaching out to Steve. Please expect a reply in 12-72 hours')
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
		payload = {'access_token': 'eo7JS8SGD49rKodcvUHPyFRnSWH1IVeZyOqUMrxU'}
		r = requests.post(url, files=files, params=payload)
		imageurl = r.json()['payload']['url']
		os.remove(filename)
		return imageurl

	
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
    pos = 0
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
    string = 'New game has been started with ' + str(len(tagged)) + ' people' + members[str(tagged[i])]['name'] + ' is up first!'
    return string

def roll(num):
    dice = ['-','-','-','Left','Center','Right']
    if num > 3:
        num = 3
    die = []
    for i in range(0,num):
        die.append(random.choice(dice))
    return die

def distribute(die, pos):
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
    nextUp = playerUp(lcr['Players'], pos)
    message += nextUp + ' is now up!'
    return message

def starting_with(arr, start_index):
     # use xrange instead of range in python 2
    for i in range(start_index, len(arr)):
        yield arr[i]
    for i in range(start_index):
        yield arr[i]

def playerUp(list, pos):
    player = ''
    for value in starting_with(list, pos + 1):
        if player == '':
            if value['chips'] > 0:
                player = value['name']
                value['turn'] = 1
                
    return player

def scoreboard():
    score = ''
    for i in range(len(lcr['Players'])):
        score += lcr['Players'][i]['name'] + ': ' + str(lcr['Players'][i]['chips']) + '\n'
    return score

def gameOver():
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
    return message

def turn():
    for i in range(len(lcr['Players'])):
        if lcr['Players'][i]['turn'] == 1:
            
            return lcr['Players'][i]['userId'], lcr['Players'][i]['name']
	
def position(sender_id):
    pos = 0
    for i in range(len(lcr['Players'])):
        if sender_id == lcr['Players'][i]['userId']:
            pos = i
    return pos



# Checks whether the message sender is a bot
def sender_is_bot(message):
	return message['sender_type'] == "bot"
