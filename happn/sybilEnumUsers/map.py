import pygmaps
import time
import math

mymap = pygmaps.maps(40.703313, -73.979681, 16)

width = 3
height = 3
lat = 40.703313
lon = -73.979681

sybils = [1,2]


#Each sybil will be seperated by 1000m (twice default radius) and proceed longitudinaly    
lConvFactor_km  = 110.0       # Conversion fator to degrees lat/lon in km
lConvFactor_m   = 111000.0    # Conversion fator to degrees lat/lon in m
r_m = 500
r_l = r_m*2 / lConvFactor_m   # Conversion to degrees lat/lon

targetLat = lat + (width / lConvFactor_km)
targetLon = lon + (height / lConvFactor_km)

print (targetLat,targetLon)

mymap = pygmaps.maps(lat, lon, 14)
mymap.addpoint(lat, lon, "#FFFF00")
mymap.addpoint(targetLat, targetLon, "#00FFFF")

# Generate sybil positions
x=[lat]
y=lon 
for __ in range(1,len(sybils)):
    x.append(x[-1]+r_l)     


s_km_count = 0  #Progress counter
while max(x) < targetLat:
    y = lon

    while y < targetLon:

        for idx, user in enumerate(sybils):            
            mymap.addradpoint(x[idx], y, r_m, "#000000")
        
        y+=r_l;
        print y            

    for idx in range(0,len(x)):
        x[idx]+= len(x)*r_l

print x,y 
#mymap.addradpoint(x[idx], y, r_m, "#FF0000")

mymap.draw('./mymap.html')