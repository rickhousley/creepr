#!/usr/bin/env python

""" sybilSupriseDate.py """

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
	'Connection':'Keep-Alive',
	'Accept-Encoding':'gzip'
}

#Phone specific IDs for generating
client_id = 'FUE-idSEP-f7AqCyuMcPr2K-1iCIU_YlvK-M-im3c'
client_secret = 'brGoHSwZsPjJ-lBk0HqEXVtb3UFu-y5l_JcOjD-Ekv'

def main(args):

	# Instantiate Logger	
	logging.basicConfig(filename='log.log', level=logging.DEBUG)
	# Create logger file handler
	logging.debug('Logger initiated')

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
			logging.warning('Error creating sybil, moving on to next token')
	if sybils == []:
		logging.warning('No Sybils to work with, exiting')
		return

	# Calculate Sybil# of equidistant lat/lon pairs from centroid
	# @TODO pass in centroid value
	r = args.radius # in meters
	vertices = len(sybils)
	xcentroid = args.clat
	ycentroid = args.clon
	slsl = 111000 #SingleLatSingleLon
	xcoord = [(r*np.cos((x * 2 * np.pi)/vertices)/slsl + xcentroid) for x in range(0,vertices)]
	ycoord = [(r*np.sin((y * 2 * np.pi)/vertices)/slsl + ycentroid) for y in range(0,vertices)]

	coords = zip(xcoord,ycoord)
	print coords

	# Update sybil locations and get distances
	for sybil,coord in zip(sybils,coords):
		sybil.setLocation(coord[0],coord[1])
		sybil.getDistance()

	#Mapping for debugging
	if args.mapping:
		# Centroid
		mymap = pygmaps.maps(42.3437217, -71.0913747, 16)
		mymap.addpoint(42.3437217, -71.0913747, "#FFFFFF")

		# Plot Sybils and their associative distances
		for sybil in sybils:
			mymap.addpoint(sybil.lat, sybil.lon, "#000000")				
			print 'mapped'			
		
		mymap.draw('mymap.draw.html') 
		url = 'mymap.draw.html'
		webbrowser.open_new_tab(url) 

class Sybil:
	""" Fake user class - one controller - Sybil """	

	def __init__(self, fbtoken):		
		self.fbtoken = fbtoken
		self.oauth = self.getOAuth()
		if self.oauth == False:
			# Unale to authenticate, return no sybil
			raise NameError('OAuth fail')
			
		self.lat = 0
		self.lon = 0
		self.distance = 0

	def setLocation(self, latitude, longitude):
		""" Set the position of the Sybil using Happn's API """

	 	h=headers
	 	h.update({'Content-Length' : 54})
 		url = 'https://api.happn.fr/api/users/1830653747/position/'
 		payload = {
 			"alt": 0.0,
			"latitude": latitude,
 			"longitude": longitude
 		}
 		r = requests.post(url,headers=h,data=payload)
 		
 		# Check status of Position Update
 		if r.status_code == 200:
 			# If success, set self.lat and self.lon
 			self.lat = latitude
 			self.lon = longitude
 			
 			print 'change pos success'
 		else:
 		# Status failed, get the current location according to the server
 			#@TODO IMPLEMENT ^ 			
 			self.lat = latitude
 			self.lon = longitude
 			print 'no success in pos change'


	def getDistance(self, userID):
		""" Gets the distance from the sybil"""
	 	h=headers
	 	h.update({'Content-Type':'application/json'})
	 	query = urllib2.quote('query={"fields":"distance"}')
	 	url = 'https://api.happn.fr/api/users/' +str(userID) + query
	 	
	 	try:
	 		r = requests.get(url, headers=h)
	 	except:
	 		logging.warning('Error creating connection to Happn server')
	 		return False

	 	if r.status_code == 200:
	 		# Succesfully got distance
	 		self.distance = r.json()['distance']
	 	else:
	 		logging.warning('Server denied request for user distance')
	 		self.distance = -1;
	 		return False

		self.distance()
		print 'IMPLEMENT THIS'
 		
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


		if r.status_code == 200:
			# Succesfully got oauth token
			self.oauth = r.json()['access_token']
			logging.info('Fetched Happn OAuth token:, %s', self.oauth)
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
	parser.add_argument('--cLat', type='int',
		dest='clat', default=42.3437217,
		help='Centroid latitude')

	parser.add_argument('--cLon', type='int',
		dest='clon', default=-71.0913747,
		help='Centroid longitude')

	parser.add_argument('--radius', type='int',
		dest='radius', default=1000,
		help='Radius of sybils from centroid')

	# Enable mapping
	parser.add_argument('--mapping', action='store_true',
		dest='mapping', default=None,
		help='Enable mapping of sybil placement')

	args = parser.parse_args()	
	main(args)