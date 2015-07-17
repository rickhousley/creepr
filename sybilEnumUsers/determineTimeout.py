#!/usr/bin/env python

""" determineTimeout.py """
# Determine timeouts between position sets
# :param fbToken Facebook token

__author__ = "Rick Housley"


import happn
from datetime import datetime
import time
import argparse

def main(args):
    # Create user object
    user = happn.User(args.token)

    # Set user position, start stopwatch
    user.set_device()
    try:
        user.set_position(42.3425227,-71.0885269)                         
    except happn.HTTP_MethodError as e:
        print 'Unable to change position due to HTTP method error: {}'.format(e.value)
        #return False
    start = datetime.now()  
    
    count = 0
    while True:
        # Set user position
        print "{} Attempts".format(count)
            
        try:
            user.set_device()
            time.sleep(10)
            user.set_position(20.3425227,-157.0885269)
        except happn.HTTP_MethodError as e: 
            time.sleep(60)
            count = count + 1
            continue
        break

    end = datetime.now()        

    print "Start Time: {}".format(start)
    print "End Time: {}".format(end)


if __name__ == '__main__':          
    # Generate argparse menu
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--token', required=True,
        dest='token', default=None,
        help='Facebook user token')

    args = parser.parse_args()  
    main(args)

#--Results from my test
# 0 Attempts
# 1 Attempts
# 2 Attempts
# 3 Attempts
# 4 Attempts
# 5 Attempts
# 6 Attempts
# 7 Attempts
# 8 Attempts
# 9 Attempts
# 10 Attempts
# 11 Attempts
# 12 Attempts
# 13 Attempts
# 14 Attempts
# 15 Attempts
# 16 Attempts
# 17 Attempts
# 18 Attempts
# 19 Attempts
# 20 Attempts
# Start Time: 2015-02-21 12:23:13.301270
# End Time: 2015-02-21 12:43:31.162098

# 20 minutes 18 seconds 