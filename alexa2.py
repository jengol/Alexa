# FLASK PORTION

import logging

from random import randint

from flask import Flask, render_template

from flask_ask import Ask, statement, question, session

app = Flask(__name__)

ask = Ask(app, "/")

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

#Start of program

@ask.launch

def new_game():

    welcome_msg = render_template('welcome')

    return question(welcome_msg)

@ask.intent("YesIntent")

def next_round():

    prompt_msg = render_template('prompt')

    return question(prompt_msg)

isPos = 0


@ask.intent("AIntent")

def answer():
    
    isPos = 1
    # return question(feeling)
    return statement("Moving on")

app.run(debug=True)
# SENTIMENT ANALYSIS AND TWILIO PORTION

from textblob import TextBlob
import json
from twilio.rest import TwilioRestClient
from random import randint


#create a struct 
from collections import namedtuple
polarity_object = namedtuple("polarity_object", "line_number polarity") #similar to creating a struct in C


#twilio logistical code
account = "AC9bc222e4739b55006abd25806bd818a8"
token = "2914f6004c52b9fd9e8c4347b587d4cc"
client = TwilioRestClient(account, token)

#load in buzzfeed's data
json_file = 'buzzfeed_headlines.json'    #string
json_data = open(json_file)              #opens the file
i = 0


pos = []    #list of pos polarities
neg = []    #list of neg polarities

for line in json_data:
    f = json.loads(line)
    if isinstance(f["blurb"],basestring):
        blob = TextBlob(f["blurb"])
    else:
        continue
    if blob.sentiment.polarity > 0:
        pos.append(polarity_object(i,blob.sentiment.polarity))
    else: 
        neg.append(polarity_object(i,blob.sentiment.polarity))
    i = i + 1
    if i == 1000: # For testing purposes: otherwise this would take forever to run
        break

# isPos = 1
#generate random number to pick article from (0,100)
random_article = randint(0,100)


if(isPos):
    ln = pos[random_article].line_number

    print('Happy article, Polarity:')
    print(str(pos[random_article].polarity))
else:
    ln = neg[random_article].line_number
    print('Sad article, Polarity: ')
    print(str(neg[random_article].polarity))

for i, line in enumerate(json_data):
    if i == ln:
        f = json.loads(line)
        url = f["uri"]
        headline = f["name"]
        break

url = 'https://www.buzzfeed.com/buzz/' + url


#MORE FLASH
requestMessage = 1

#Tell them the article name and ask if they want to be sent a link
def article_echo():

    article = render_template("article_name")
    send_link = render_template("send_link")
    q = article + headline + send_link
    return question(q) 



@ask.intent("YesIntent")

def url_boolean():
    requestMessage = 1


if(requestMessage and isPos):
    print(url)
    message = client.messages.create(to="+17327665931", from_="+17185718615", body=url)
elif(requestMessage and not isPos):
    print(url)
    message = client.messages.create(to="+17327665931", from_="+17185718615", body=url)


#End of program
json_data.close()