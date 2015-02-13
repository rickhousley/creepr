import matplotlib.pyplot as plt
import numpy as np
import math as m
import pygmaps 
import webbrowser 

r = 10000 # in meters
vertices = 10
xcentroid = 42.3437217
ycentroid = -71.0913747
slsl = 111000 #SingleLatSingleLon
xcoord = [(r*np.cos((x * 2 * np.pi)/vertices)/slsl + xcentroid) for x in range(0,vertices)]
ycoord = [(r*np.sin((y * 2 * np.pi)/vertices)/slsl + ycentroid) for y in range(0,vertices)]

coords = zip(xcoord,ycoord)

#Mapping for debugging
mapping = True
if mapping==True:
	mymap = pygmaps.maps(42.3437217, -71.0913747, 16)
	mymap.addpoint(42.3437217, -71.0913747, "#FFFFFF")

	for point in coords:
		mymap.addpoint(point[0], point[1], "#000000")	
	
	mymap.draw('mymap.draw.html') 
	url = 'mymap.draw.html'
	webbrowser.open_new_tab(url) 
