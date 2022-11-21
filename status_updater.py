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
    parser.add_option("-a", "--alloc_id", help="Allocation id of the request")
    parser.add_option("-r", "--request_id", help="Request id to update")
    parser.add_option("-o", "--object_id", help="Object id of the request")
    parser.add_option("-s", "--status", help="Status of the request", type=int)
    parser.add_option("-t", "--token", help="Fritz/skyportal token, required")

    opts, args = parser.parse_args()

    return opts


# Parse command line
opts = parse_commandline()
if not opts.request_id:
    print('--request_id is required, exiting')
    sys.exit()
if not opts.alloc_id:
    print('--alloc_id is required, exiting')
    sys.exit()
if not opts.object_id:
    print('--object_id is required, exiting')
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
method = 'POST'
session = requests.Session()

status = {0: "Complete", 1: "Interrupted", 2: "Skipped"}
if opts.status not in status.keys():
    print('Invalid status, exiting')
    sys.exit()

endpoint = f'followup_request/{opts.request_id}'
url = urllib.parse.urljoin(opts.host, f'/api/{endpoint}')
params = {'allocation_id': opts.alloc_id,
          'obj_id': opts.object_id,
          'status': status[opts.status]}

response = session.request(method, url, params=params, headers=headers)
if response['status']=="success":
    print(f'Successfully updated request {opts.request_id}')
else:
    print(f'Error in updating request {opts.request_id}')

