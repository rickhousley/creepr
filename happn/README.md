#Happn

##sybilSupriseDate.py

####Command Line Arguments
```
usage: sybilSupriseDate.py [-h] --fbTokenFile FBTOKENFILE --userID USERID
                           [--cLat CLAT] [--cLon CLON] [--radius RADIUS]
                           [--mapping]

optional arguments:
  -h, --help            show this help message and exit
  --fbTokenFile FBTOKENFILE
                        File containing a list of facebook access tokens
  --userID USERID       UserID of user to track
  --cLat CLAT           Centroid latitude
  --cLon CLON           Centroid longitude
  --radius RADIUS       Radius of sybils from centroid
  --mapping             Enable mapping of sybil placement
```

####Design Explanation

####Additional notes

####To Do

* Fixes
	* Generated map .html should be named <uid>.html
* Features
	* Multilateration
	* Facebook Auth
* Other
	* Document all functions
	* Finish README


##Happn Vuln Notes
####Legacy API Leak

