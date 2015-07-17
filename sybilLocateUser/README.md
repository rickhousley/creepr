####Command Line Arguments
```
usage: sybilLocateUser.py [-h] --fbTokenFile FBTOKENFILE --userID USERID
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
  python sybilLocateUser.py --fbTokenFile tokens --userID 1346023834
```

click [here](https://www.facebook.com/dialog/oauth?client_id=464891386855067&redirect_uri=https://www.facebook.com/connect/login_success.html&scope=basic_info,email,public_profile,user_about_me,user_activities,user_birthday,user_education_history,user_friends,user_interests,user_likes,user_location,user_photos,user_relationship_details&response_type=token) to get Facebook token. Load a file with multiple users' Facebook tokens to get hire accuracy on user locating

####Design Explanation
A user's location can be detrmined if the user is a known distance from at least three other users in unique locations. Using (multilateration)[] the user's position can be calculated. The more users provided, the higher the degree of tracking accuracy. This progam generates a number of fake Happn users and spawns them equidistantly from a given centroid.

__Given 3 Facebook Tokens, a 100m radius, and lat,lon__

__Given 8 Facebook Tokens, a 100m radius, and lat,lon__

__Program Flow:__
```
        Load Facebook Tokens
                |
          Generate Sybils
                |
  Calculate Locations around Centroid
                |
          For each Sybil
                |
        1. Update Activity
                |
          2. Set Device
                |
  3. Set Location around Centroid
                |
          4. Get Distance
                |
    Multilateration Calculation *Not yet completed*
                |
  Map Sybil Placement and Target

```
####Additional notes

####To Do

* Fixes
    * ~~Generated map .html should be named <uid>.html~~
* Features
    * Multilateration
    * Facebook Auth
    * Extended Tracking
    * Geopy reverse locating
    * ~~Add HTTP Status code interpretations~~
* Other
    * ~~Document all function~~ 
    * Finish README
      - Insert equidistant map example in readme
