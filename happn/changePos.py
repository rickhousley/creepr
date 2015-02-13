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
 			
 			logging.info('Set sybil position at %d, %d', self.lat, self.lon)
 		else:
 			# Status failed, get the current location according to the server
 			#@TODO IMPLEMENT ^ 			
 			self.lat = latitude
 			self.lon = longitude
	 		logging.warning('Server denied request for position change: %d', r.status_code)
