#!/usr/bin/env python

""" happnCrackin.py """

__author__      = "Rick Housley"
__copyright__   = "Copyright 2015"

import logging
import argparse
import json
import requests
import urllib2

headers = {
	'http.useragent':'Happn/1.0 AndroidSDK/0',
	'Authorization':'OAuth="e922bc17546a86baff4b3c13785bf68a02"',
	'Content-Type':'application/json',
	'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SCH-I535 Build/KOT49H)',
	'Host':'api.happn.fr',
	'Connection':'Keep-Alive',
	'Accept-Encoding':'gzip'
}

def main(args):	
	# Inititate Logging
#	logging.basicConfig(filename='happn.log', level=logging.DEBUG)
#	now = datetime.datetime.now()	
#	logging.info('\n\n--Program Inititated at %s', str(now))			
#	findInfo(args.userID)	
	changeLocation(42.340355,-71.085806)

def findInfo(userID):
	h=headers	
	url = 'https://api.happn.fr/api/users/'+str(userID) +'?query=%7B%22fields%22%3A%22first_name%2Clast_name%2Cgender%2Cunread_conversations%22%7D'
	r = requests.get(url, headers=h)
	print json.dumps(r.json(), indent=4, separators=(',', ': '))

def getRecs(numRecs):
	h=headers
	url = 'https://api.happn.fr/api/users/1830653747/notifications/?query='
	query = '{"types":"468","limit":1000,"offset":0,"fields":"id,modification_date,notification_type,nb_times,notifier.fields(id,distance,gender,first_name,last_name,age)"}'
	query = urllib2.quote(query)
	r = requests.get(url+query,headers=h)
	#print r
	print json.dumps(r.json(), indent=4, separators=(',', ': '))		


def changeLocation(lat,lon):
	h=headers
	h.update({'Content-Length' : 54})
	url = 'https://api.happn.fr/api/users/1830653747/position/'
	dat={
		"alt": 0.0,
    	"latitude": lat,
		"longitude": lon
	}
	print dat
	r = requests.post(url,headers=h,data=dat)
	print r

if __name__ == '__main__':
	#Generate argparse menu
	parser = argparse.ArgumentParser()

	# Link chaff option
	parser.add_argument('--findinfo', metavar='f',
		dest='userID', default=None, type=int,
		help='UserID to get')
	
	args = parser.parse_args()

	main(args)