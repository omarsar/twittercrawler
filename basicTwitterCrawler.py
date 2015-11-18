import requests
import json
import urllib
import sys
import os
import codecs
import json
import re
import csv
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

#Consumer Key
ckey = 'YOUR_CONSUMER_KEY'
#Consumer Secret
csecret = 'YOUR_CONSUMER_SECRET'
#Access Token
atoken = 'YOUR_ACCESS_TOKEN'
#Acces Secret
asecret = 'YOUR_ACCESS_SECRET'

class listener(StreamListener):
	def on_data(self, data):
		try:	
			language = "other"
			convtweet= []
			convtweet = json.loads(data)
			try:
				language = convtweet['lang']
			except:
				print ("didnt capture language")
			
			anyretweet= re.findall(r'RT', str(convtweet['text']))
	
			#only support english tweets and non-Retweets
			if language == "en" and not anyretweet :
	
				textoftweet = convtweet['text']
				print (textoftweet)

				saveThistofile = open('tweetscrawled.csv','a')
				sthiscsv = csv.writer(saveThistofile,delimiter=',')
				
				#Classify tweet into pertaining emotin upon cralwing
				try:
					payload = {"lang":"und","text":textoftweet}
					url = 'EMOTION_API_URL'
					try:
						r = requests.post(url, data=json.dumps(payload))
					except Exception:
						r = requests.post(url, data=json.dumps(payload))
						pass
					r= r.json()
					
					emodesc=""

					descrips = r['groups'][0]['emotions']

					for test in descrips:
						emodesc+=str(test+" ")

					try:
						sthiscsv.writerow([r['text'].encode('utf8'),r['groups'][0]['name'],\
						emodesc])

					except Exception:
						print ("writing to file failed")
						pass
				except Exception:
					print ("the url thingy failed")
					pass
			
			return True
		except Exception:
			return True

	def on_error(self, status):
		print (status)
		return True
		return False

	def on_timeout(self):
	    print >> sys.stderr, 'Timeout...'
	    return True # Don't kill the stream   
	    return False

	def on_status(self, status):
		print (status.text)

############################
# Main Function of Crawler
############################

#Continuous Crawler
while True:
	try:
		auth = OAuthHandler(ckey, csecret)
		auth.set_access_token(atoken, asecret)
		twitterStream = Stream(auth, listener())
		track = ['FIFA','fifa',] #Keyword to track (you can provide multiple keywords separated by a comma)
		twitterStream.filter(track=track)
	except:
		continue
