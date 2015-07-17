#!/usr/bin/env python

""" sybilSupriseDate.py """
# @TODO add http status code meanings

__author__      = "Rick Housley"

import logging
import argparse
import json
import requests
import urllib2
import logging
import datetime
import argparse 			# Command line menu
import matplotlib.pyplot as plt
import numpy as np
import math as m
import pygmaps 
import webbrowser 

# Headers that will be used by all three Sybils
headers = {
	'http.useragent':'Happn/1.0 AndroidSDK/0',	
	'User-Agent':'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SCH-I535 Build/KOT49H)',	
	'Host':'api.happn.fr',	
	'connection' : 'Keep-Alive',
	'Accept-Encoding':'gzip'
}

#Phone specific IDs for generating oauth tokens
client_id = 'FUE-idSEP-f7AqCyuMcPr2K-1iCIU_YlvK-M-im3c'
client_secret = 'brGoHSwZsPjJ-lBk0HqEXVtb3UFu-y5l_JcOjD-Ekv'

def main(args):
	# Instantiate Logger	
	logging.basicConfig(filename='log.log', level=logging.INFO)
	logging.info('--------------------Logger Initiated--------------------')

	# Load facebook tokens from a file
	fbtokens = None
	try:
		with open(args.fbTokenFile) as f:
			fbtokens = f.read().splitlines()
	except IOError:
		logging.warning('Unable to locate file provided')
		return

	if fbtokens is None:
		logging.warning('Token file void of tokens')		
		return
	else:
		logging.info('%d Facebook tokens loaded from file',len(fbtokens))

	# Create a list of Sybils
	sybils = []
	for token in fbtokens:	
		try:		
			sybils.append(Sybil(token))			
		except NameError:
			logging.warning('Error creating sybil, moving on to next token (most likely invalid token)')
	if sybils == []:
		logging.warning('No Sybils to work with, exiting')
		return
	logging.info('Completed sybil generation')

	# Calculate Sybil # of equidistant lat/lon pairs from centroid
	r = args.radius # in meters
	vertices = len(sybils)
	xcentroid = args.clat
	ycentroid = args.clon
	slsl = 111000 #SingleLatSingleLon
	xcoord = [(r*np.cos((x * 2 * np.pi)/vertices)/slsl + xcentroid) for x in range(0,vertices)]
	ycoord = [(r*np.sin((y * 2 * np.pi)/vertices)/slsl + ycentroid) for y in range(0,vertices)]
	coords = zip(xcoord,ycoord)

	# Update sybil locations and get distances
	for sybil,coord in zip(sybils,coords):
		sybil.updateActivity()
		sybil.setDevice()
		sybil.setLocation(coord[0],coord[1])
		sybil.getDistance(args.userID)

	#Mapping for debugging
	if args.mapping:
		# Centroid
		mymap = pygmaps.maps(xcentroid, ycentroid, 16)
		mymap.addpoint(xcentroid, ycentroid, "#FFFFFF")

		# Plot Sybils and their associative distances
		for sybil in sybils:
			mymap.addpoint(sybil.lat, sybil.lon, "#000000")				
			mymap.addradpoint(sybil.lat, sybil.lon, sybil.distance, "#000000")
		
		
		mymap.draw('mymap.draw.html') 
		url = 'mymap.draw.html'
		webbrowser.open_new_tab(url) 

class Sybil:
	""" Fake user class - one controller - Sybil """	

	def __init__(self, fbtoken):		
		self.fbtoken = fbtoken
		self.id = 0
		self.oauth = self.getOAuth()
		if self.oauth == False:
			# Unale to authenticate, return no sybil
			raise NameError('OAuth fail')			
		self.lat = 0
		self.lon = 0
		self.distance = 0
		logging.info('Sybil Generated. ID: %s', self.id)

	def setLocation(self, latitude, longitude):
		""" Set the position of the Sybil using Happn's API """

	 	h=headers	 	
	 	h.update({'Authorization' : 'OAuth="'+ self.oauth + '"',
	 	  'Content-Length' : 53,
	 	  'Content-Type' : 'application/json'})

 		url = 'https://api.happn.fr/api/users/' + self.id + '/position/' 		

 		payload = {
 			"alt": 0.0,
			"latitude": 42.34257,
 			"longitude": -71.08823
 		} 	
 		r = requests.post(url,headers=h,data=json.dumps(payload))
 		
 		# Check status of Position Update
 		if r.status_code == 200:
 			# If success, set self.lat and self.lon
 			self.lat = latitude
 			self.lon = longitude
 			
 			logging.info('Set sybil position at %d, %d', self.lat, self.lon)
 		else:
 			# Status failed, get the current location according to the server
 			#@TODO IMPLEMENT ^ 			
 			self.lat = latitude
 			self.lon = longitude
	 		logging.warning('Server denied request for position change: %d', r.status_code)

	def setDevice(self):
		h=headers
		h.update({
		  'Authorization' : 'OAuth="'+ self.oauth + '"',
	 	  'Content-Length' : 342,
	 	  'Content-Type' : 'application/json'})
		payload ={
		    "app_build": "18.0.11", 
		    "country_id": "US", 
		    "gps_adid": "05596566-c7c7-4bc7-a6c9-729715c9ad98", 
		    "idfa": "f550c51fa242216c", 
		    "language_id": "en", 
		    "os_version": 19, 
		    "token": "APA91bE3axREMeqEpvjkIOWyCBWRO1c4Zm69nyH5f5a7o9iRitRq96ergzyrRfYK5hsDa_-8J35ar7zi5AZFxVeA6xfpK77_kCVRqFmbayGuYy7Uppy_krXIaTAe8Vdd7oUoXJBA7q2vVnZ6hj9afmju9C3vMKz-KA", 
		    "type": "android"
		}
		url = 'https://api.happn.fr/api/users/' + self.id + '/devices/1830658762'
		r = requests.put(url,headers=h,data=json.dumps(payload))

		# Check status of device set
 		if r.status_code == 200:
 			logging.info('Device Set')
 		else:
 			# Device set denied by server
	 		logging.warning('Server denied request for device set change: %d', r.status_code)


	def getDistance(self, userID):
		""" Gets the distance from the sybil"""
	 	h={
		 	'http.useragent':   'Happn/1.0 AndroidSDK/0',
			'Authorization':    'OAuth="' + self.oauth+'"',
			'Content-Type':     'application/json',
			'User-Agent':       'Dalvik/1.6.0 (Linux; U; Android 4.4.2; SCH-I535 Build/KOT49H)',
			'Host':             'api.happn.fr',
			'Connection':       'Keep-Alive',
			'Accept-Encoding':  'gzip'
	 	}
	 	query = '?query=%7B%22fields%22%3A%22about%2Cis_accepted%2Cage%2Cjob%2Cworkplace%2Cmodification_date%2Cprofiles.mode%281%29.width%28720%29.height%281280%29.fields%28url%2Cwidth%2Cheight%2Cmode%29%2Clast_meet_position%2Cmy_relation%2Cis_charmed%2Cdistance%2Cgender%2Cmy_conversation%22%7D'
	 	url = 'https://api.happn.fr/api/users/' + userID + query	 

	 	try:
	 		r = requests.get(url, headers=h)
	 	except:
	 		logging.warning('Error creating connection to Happn server for distance query')
	 		return False

	 	if r.status_code == 200:
	 		# Succesfully got distance	 		
	 		self.distance = r.json()['data']['distance']
	 		logging.info('Sybil %d m from target',self.distance)
	 	else:
	 		logging.warning('Server denied request for user distance: %d', r.status_code)
	 		self.distance = -1;
	 		return False
		
	def updateActivity(self):
		""" Updates sybil happn activity """
		h = headers
		h.update({
			'Authorization' : 'OAuth="'+ self.oauth + '"',
			'Content-Type' : 'application/x-www-form-urlencoded; charset=UTF-8',
			'Content-Length' :   '20'
		})
		payload = {
			'update_activity' :  'true'
		}
		url = 'https://api.happn.fr/api/users/'+self.id
	 	try:
	 		r = requests.put(url, headers=h, data = payload)
	 	except:
	 		logging.warning('Error creating connection to Happn server')
	 		return False

	 	if r.status_code == 200:
	 		# Succesfully got distance
	 		logging.info('Updated sybil activity')
	 	else:
	 		logging.warning('Server denied update activity PUT: %d', r.status_code)	 
	 		logging.warning('		%s', url)		
	 		return False


 		
	def getOAuth(self):
		""" Gets the OAuth tokens using Happn's API """
		h=headers
		# Update OAuth specific headers
		h.update({'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'})
		h.update({'Content-Length': '439'})

		payload = {
			'client_id' : client_id,
			'client_secret' : client_secret,
			'grant_type' : 'assertion',
			'assertion_type' : 'facebook_access_token',
			'assertion' : self.fbtoken,
			'scope':'mobile_app'
		}
		url = 'https://api.happn.fr/connect/oauth/token'
		try:
			r = requests.post(url,headers=h,data=payload)
		except:
			logging.warning('Error creating connection to Happn server')
			# Without auth token cant use sybil
			return False

		# Check response validity
		if r.status_code == 200:
			# Succesfully got oauth token			
			self.id = r.json()['user_id']
			logging.info('Fetched Happn OAuth token:, %s', r.json()['access_token'])
			return r.json()['access_token']
		else:
			# Error code returned from server (but server was accessible)
			loggging.warning('Server denied request for OAuth token. Status: %d', r.Status)
			# Return False

if __name__ == '__main__':		

	# Create args
	# Generate argparse menu
	parser = argparse.ArgumentParser()

	# FB token 
	parser.add_argument('--fbTokenFile', required=True,
		dest='fbTokenFile', default=None,
		help='File containing a list of facebook access tokens')

	parser.add_argument('--userID', required=True,
		dest='userID', default=None,
		help='UserID of user to track')

	# FB token 
	parser.add_argument('--cLat', type=int,
		dest='clat', default=42.3437217, help='Centroid latitude')

	parser.add_argument('--cLon', type=int,
		dest='clon', default=-71.0913747, help='Centroid longitude')

	parser.add_argument('--radius', type=int,
		dest='radius', default=1000,
		help='Radius of sybils from centroid')

	# Enable mapping
	parser.add_argument('--mapping', action='store_true',
		dest='mapping', default=None,
		help='Enable mapping of sybil placement')

	args = parser.parse_args()	
	main(args)


# Link for getting FB token:
# https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token

#2491316262 Test track id
#1346023834
#https://api.happn.fr/api/users/2491316262?query=%7B%22fields%22%3A%22about%2Cis_accepted%2Cage%2Cjob%2Cworkplace%2Cmodification_date%2Cprofiles.mode%281%29.width%28720%29.height%281280%29.fields%28url%2Cwidth%2Cheight%2Cmode%29%2Clast_meet_position%2Cmy_relation%2Cis_charmed%2Cdistance%2Cgender%2Cmy_conversation%22%7D
