#!/usr/bin/env python

""" enumUsers.py 

    Enumerates all of the users in a given area.

    IN PROGRESS - NOT YET OPERATIONAL   
"""
# Set position of a given user
# :param fbToken Facebook token
# :param lat Latitude to place user at
# :param lon Longitude to place user at

__author__ = "Rick Housley"

import happn
import time
import argparse
import logging
import sys
from pymongo import MongoClient

_server_retry_rate = 120  # in s


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

    logging.info('%d Facebook tokens loaded from file', len(fbtokens))


    # Connect to database
    client = MongoClient('localhost', 27017)
    db = client.db
    db_users = db.userbase

    # Create a list of Sybils
    sybils = []
    for token in fbtokens:
        try:
            sybils.append(happn.User(token))
        except NameError:
            logging.warning(
                'Error creating sybil, moving on to next token (most likely invalid token)')

    if sybils == []:
        logging.warning('No Sybils to work with, exiting')
        return

    logging.info('Completed sybil generation')

    # Each sybil will be seperated by 1000m (twice default radius) and proceed longitudinaly
    lConvFactor_km = 110.0  # Conversion fator to degrees lat/lon in km
    lConvFactor_m = 110000.0  # Conversion fator to degrees lat/lon in m
    r_m = 500
    r_l = r_m * 2 / lConvFactor_m  # Conversion to degrees lat/lon

    targetLat = args.width * lConvFactor_km
    targetLon = args.height * lConvFactor_km

    # Generate sybil positions
    x = [args.lat]
    y = args.lon
    for __ in range(1, len(sybils)):
        x.append(x[-1] + r_l)


        # Calculate time to completion
    s_mi = args.width * args.height
    s_km = s_mi * 2.58999

    m_to_completion = (s_km / len(sybils)) * 21
    h_to_completion = m_to_completion / 60
    d_to_completion = h_to_completion / 24

    print("\nWith {} sybils {} mi^2 will take:\n"
          "     {} minutes\n"
          "     {} hours\n"
          "     {} days\n\n"
          .format(len(sybils), s_mi, m_to_completion, h_to_completion,
                  d_to_completion))

    s_km_count = 0  # Progress counter
    while max(x) < targetLat:
        y = args.lon

        while y < targetLon:

            for idx, user in enumerate(sybils):

                # Command line progress updates (SE inspired)
                percent = s_km_count / s_km
                bar_length = 40
                hashes = '#' * int(round(percent * bar_length))
                spaces = ' ' * (bar_length - len(hashes))
                sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces,
                                                                int(round(
                                                                    percent * 100))))
                sys.stdout.flush()

                # Try position change until it works                                
                while True:
                    try:
                        user.set_device()
                        user.set_position(x[idx], y)

                    # @TODO: Make exceptions handle differently depending on
                    # what they are
                    except:
                        time.sleep(_server_retry_rate)
                        continue
                    break
                s_km_count += 1

                # Get Recs and save to database
                recs = user.get_recommendations(limit=1000)
                logging.info('Got %d recs', len(recs))

                # Load database with new recs
                added_count = 0
                for doc in recs:
                    # add sector for later doing data analysis
                    doc['sector'] = (x[idx], y)

                    # Check if ID already in DB (prevent duplicates)
                    if not db_users.find_one({'id': str(doc['id'])}):
                        db_users.insert(doc)
                        added_count += 1

                logging.info('Added %d unique users to the db', added_count)

            y += r_l;

        # This is ugly, do this properly with functional programming
        for idx in range(0, len(x)):
            x[idx] += len(x) * r_l

    logging.info('Completed area traversal.')


if __name__ == '__main__':
    # Generate argparse menu
    parser = argparse.ArgumentParser()

    parser.add_argument('--fbTokenFile', required=True,
                        dest='fbTokenFile', default=None,
                        help='File loaded with Facebook tokens')

    parser.add_argument('--rLat', type=float, required=True,
                        dest='lat',
                        help='Right corner latitude (starting point)')

    parser.add_argument('--rLon', type=float, required=True,
                        dest='lon',
                        help='Right corner longitude (starting point)')

    parser.add_argument('--width', type=float, required=True,
                        dest='width', help='Width to traverse in kilometers')

    parser.add_argument('--height', type=float, required=True,
                        dest='height', help='height to traverse in kilometers')

    args = parser.parse_args()
    main(args)
