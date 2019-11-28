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
	if 1+1 == 2 and not sender_is_bot(message):
		reply(message)
	
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
			
	if len(tagged) > 0:
		if '8712430' in tagged:
			reply('Thanks for reaching out to Emily')
	if message['system'] == True# and 'added' in message['text']:
		name = re.findall('added (.*?) to the',message['text'])[0].strip()
		reply('Welcome to the group, ' + name)
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

# Checks whether the message sender is a bot
def sender_is_bot(message):
	return message['sender_type'] == "bot"
