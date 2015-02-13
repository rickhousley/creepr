#Happn
##Files
* README.md	- this
* log.log 	- example log of sybilSupriseDate.py after being run
* sybilSupriseDate	- Main python script for locating a user
* tokens	- file containing a list of Facebook tokens (should be stale, dont bother)
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

Sample Run:
```
  python sybilSupriseDate.py --fbTokenFile tokens --userID 1346023834
```

click [here](https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token) to get Facebook token

####Design Explanation

####Additional notes

####To Do

* Fixes
	* Generated map .html should be named <uid>.html
* Features
	* Multilateration
	* Facebook Auth
	* Extended Tracking
  * Add HTTP Status code interpretations
* Other
	* Document all functions
	* Finish README


##Happn Vuln Notes
####Legacy API Leak

