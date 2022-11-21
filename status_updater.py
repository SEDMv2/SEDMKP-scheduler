#!/usr/bin/env python

import numpy as np
import optparse
import urllib
import requests
import sys

def parse_commandline():
    """
    Parse the options given on the command-line.
    """
    parser = optparse.OptionParser()
    parser.add_option("-w", "--host", default="https://fritz.science",
                      help="Host url for skyportal instance, by default fritz")
    parser.add_option("-r", "--request_id", help="Request id to update")
    parser.add_option("-s", "--status", help="Status of the request", type=int)
    parser.add_option("-t", "--token", help="Fritz/skyportal token, required")

    opts, args = parser.parse_args()

    return opts


# Parse command line
opts = parse_commandline()
if not opts.request_id:
    print('--request_id is required, exiting')
    sys.exit()
if opts.status is None:
    print('--status is required, exiting')
    sys.exit()
if opts.token:
    headers = {'Authorization': f'token {opts.token}'}
else:
    try:
        token = open('token.txt', 'r').read().strip()
        headers = {'Authorization': f'token {token}'}
    except:
        headers = None
session = requests.Session()

status = {0: "Complete", 1: "Interrupted", 2: "Skipped"}
if opts.status not in status.keys():
    print('Invalid status, exiting')
    sys.exit()

endpoint = f'followup_request/{opts.request_id}'
url = urllib.parse.urljoin(opts.host, f'/api/{endpoint}')
response = session.request('GET', url, params=None, headers=headers).json()

params = {'allocation_id': response['allocation_id'],
          'obj_id': response['obj_id'],
          'status': status[opts.status]}

response = session.request('PUT', url, params=params, headers=headers)
if response['status']=="success":
    print(f'Successfully updated request {opts.request_id}')
else:
    print(f'Error in updating request {opts.request_id}')

