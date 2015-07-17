#!/usr/bin/env python

""" sybilLocateUser.py """

__author__      = "Rick Housley"

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
			sybils.append(happn.User(token))			
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
		#sybil.updateActivity()
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
		
		
		mymap.draw(str(args.userID +'_map.html') 
		url = 'mymap.draw.html'
		webbrowser.open_new_tab(url) 