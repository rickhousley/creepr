# encoding: utf8                                                                                                                                           1,1           Top# encoding: utf8
#import argparse
from datetime import datetime
import json
from random import randint
import requests
import sys
from time import sleep
import urllib

import math
import numpy
from numpy import *
from collections import namedtuple

import time
#import datetime

headers = {
    'app_version': '3',
    'platform': 'ios',
}
 
 #curl -X POST https://api.gotinder.com/auth --data '{"facebook_token": CAAGm0PX4ZCpsBAHNCeuEyiapeC5ZAdwM5wAH7Db6BQxYLAW0WjeSul7cB39uE9pvFGbNqySUiOqFi6UvMAT7a59PaeQcwIZCUZCrmlQ9WvwT76TUUv1EsHGgyl9PkPuwi2hRhIWzNpJhzz1CnIj5zA0uVGFVDO8SXAhgCASZAebkKKmSrSZAgKpPWrzaud9s9VyzLYnXP2d6PV3cFg2jcLJT9SJkMHUVYZD, "facebook_id": 100003236020785}'
#https://www.facebook.com/connect/login_success.html#access_token=
fb_id = '100003236020785'
fb_auth_token = 'CAAGm0PX4ZCpsBAOlaP4mPIjNoegkPflG00PIakP9zRrpb29kpv9gXg4o7YNX4iUS5RTBZBu0oGkyKQ9icpPRCdpStynYvOHgAqhhHcrXmeDU0OZCMoBRuDkEyRCeX0V0C0YeZB4Mkno3ZBSWcNwB5ZA7ZCSlDBMXYwC15xFzv92ORyjZCm13fGXCCIZCK5ZAYUSkuCT9iB2rpATJJJY08r0KzZC'

class User(object):
    def __init__(self, data_dict):
        self.d = data_dict
 
    @property
    def user_id(self):
        return self.d['_id']
 
    @property
    def ago(self):
        raw = self.d.get('ping_time')
        if raw:
            d = datetime.strptime(raw, '%Y-%m-%dT%H:%M:%S.%fZ')
            secs_ago = int(datetime.now().strftime("%s")) - int(d.strftime("%s"))
            if secs_ago > 86400:
                return u'{days} days ago'.format(days=secs_ago / 86400)
            elif secs_ago < 3600:
                return u'{mins} mins ago'.format(mins=secs_ago / 60)
            else:
                return u'{hours} hours ago'.format(hours=secs_ago / 3600)
 
        return '[unknown]'
 
    @property
    def bio(self):
        try:
            x = self.d['bio'].encode('ascii', 'ignore').replace('\n', '')[:50].strip()
        except (UnicodeError, UnicodeEncodeError, UnicodeDecodeError):
            return '[garbled]'
        else:
            return x

    @property
    def image_url(self):
        raw = self.d['photos']
        url = raw[0]["processedFiles"][0]["url"]
        return url
 
    @property
    def age(self):
        raw = self.d.get('birth_date')
        if raw:
            d = datetime.strptime(raw, '%Y-%m-%dT%H:%M:%S.%fZ')
            return datetime.now().year - int(d.strftime('%Y'))
 
        return 0   

    @property
    def distance(self):
        return self.d.get('distance_mi')        
 
    def __unicode__(self):
        return u'{name} ({age}), {distance}km, {ago}, {tID}'.format(
            name=self.d['name'],
            age=self.age,
            distance=self.d['distance_mi'],
            ago=self.ago,
            tID=self.user_id
        )


def auth_token(fb_auth_token, fb_user_id):
    h = headers
    h.update({'content-type': 'application/json'})
    h.update({'User-Agent': 'Tinder/4.0.4 (iPhone; iOS 7.1.1; Scale/2.00)'})
    req = requests.post(
        'https://api.gotinder.com/auth',
        headers=h,
        data=json.dumps({'facebook_token': fb_auth_token, 'facebook_id': fb_user_id})
    )
    try:
        return req.json()['token']
    except:
        return None
 
 
def changeLocation(lat,lon, auth_token):
    #cant do super large position changes quickly
    #cant do super minor position changes
    h = headers
    h.update({'X-Auth-Token': auth_token})
    locdata = {'lat' : lat, 'lon' : lon}
    requestUrl = 'https://api.gotinder.com/user/ping'
    r=requests.post(requestUrl, headers=h,data=json.dumps(locdata))
    # print r

    # @TODO: Check if r is succesful or not (200)

def recommendations(auth_token):
    h = headers
    h.update({'X-Auth-Token': auth_token})
    
    r = requests.get('https://api.gotinder.com/user/recs', headers=h)
    if r.status_code == 401 or r.status_code == 504:
        raise Exception('Invalid code')
        print r.content
 
    if not 'results' in r.json():
        print r.json()
 
    for result in r.json()['results']:
        yield User(result)


def getSpecificUser(userID, auth_token):
    h = headers
    h.update({'X-Auth-Token': auth_token})
    requestUrl = 'https://api.gotinder.com/user/' + userID

    r=requests.get(requestUrl, headers=h)
    
    if not 'results' in r.json():
        print 'Unable to locate'
        return None
    else:
        return User(r.json()['results'])
  
def getUserLocation(targetUserID):
    #Return a tuple

    lat0 = 42.30955
    lon0 = -71.088527
    changeLocation(lat0,lon0,token)
    user = getSpecificUser(targetUserID,token)
    #print user.__unicode__()
    #print str(user.distance) + " km away"
    d1 = user.distance

    lat1 = 42.34955
    lon1 = -71.088527
    changeLocation(lat1,lon1,token)
    user = getSpecificUser(targetUserID,token)
    d2 = user.distance

    #print str(user.distance) + " km away"

    lat2 = 42.34955
    lon2 = -71.188527
    changeLocation(lat2,lon2,token)
    user = getSpecificUser(targetUserID,token)
    d3 = user.distance

    #print str(user.distance) + " km away"

    # Do trilateration - stackOverflow source
    #assuming elevation = 0
    earthR = 6371
    LatA = lat0
    LonA = lon0
    DistA = d1
    LatB = lat1
    LonB = lon1
    DistB = d2
    LatC = lat1
    LonC = lon1
    DistC = d3

    #using authalic sphere
    #if using an ellipsoid this step is slightly different
    #Convert geodetic Lat/Long to ECEF xyz
    #   1. Convert Lat/Long to radians
    #   2. Convert Lat/Long(radians) to ECEF
    xA = earthR *(math.cos(math.radians(LatA)) * math.cos(math.radians(LonA)))
    yA = earthR *(math.cos(math.radians(LatA)) * math.sin(math.radians(LonA)))
    zA = earthR *(math.sin(math.radians(LatA)))

    xB = earthR *(math.cos(math.radians(LatB)) * math.cos(math.radians(LonB)))
    yB = earthR *(math.cos(math.radians(LatB)) * math.sin(math.radians(LonB)))
    zB = earthR *(math.sin(math.radians(LatB)))

    xC = earthR *(math.cos(math.radians(LatC)) * math.cos(math.radians(LonC)))
    yC = earthR *(math.cos(math.radians(LatC)) * math.sin(math.radians(LonC)))
    zC = earthR *(math.sin(math.radians(LatC)))

    P1 = array([xA, yA, zA])
    P2 = array([xB, yB, zB])
    P3 = array([xC, yC, zC])

    #from wikipedia
    #transform to get circle 1 at origin
    #transform to get circle 2 on x axis
    ex = (P2 - P1)/(numpy.linalg.norm(P2 - P1))
    i = dot(ex, P3 - P1)
    ey = (P3 - P1 - i*ex)/(numpy.linalg.norm(P3 - P1 - i*ex))
    ez = numpy.cross(ex,ey)
    d = numpy.linalg.norm(P2 - P1)
    j = dot(ey, P3 - P1)

    #from wikipedia
    #plug and chug using above values
    x = (pow(DistA,2) - pow(DistB,2) + pow(d,2))/(2*d)
    y = ((pow(DistA,2) - pow(DistC,2) + pow(i,2) + pow(j,2))/(2*j)) - ((i/j)*x)

    # only one case shown here
    z = sqrt(pow(DistA,2) - pow(x,2) - pow(y,2))

    #triPt is an array with ECEF x,y,z of trilateration point
    triPt = P1 + x*ex + y*ey + z*ez

    #convert back to lat/long from ECEF
    #convert to degrees
    lat = math.degrees(math.asin(triPt[2] / earthR))
    lon = math.degrees(math.atan2(triPt[1],triPt[0]))

    coord = lat,lon,int(time.time())
    return coord

if __name__ == '__main__':
    token = auth_token(fb_auth_token, fb_id)
    print "token %s" % (token)   

    if token is None:
        print "error obtaining auth token"
        raise ValueError

#    for user in recommendations(token):
#        print user.__unicode__()
    
    target = '53d04ec79d11d604704aa79a'
    print getUserLocation(target)

    #Begin creepr tracking script

    with open(target+".txt", "a") as myfile:
        while True:
            location = getUserLocation(target)
            data = str(location)
            myfile.write(data)
            print data
            sleep(300)
