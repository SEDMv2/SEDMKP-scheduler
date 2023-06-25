import pandas as pd
import requests, os
import argparse
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.time import Time

def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('list', help='List of targets to create fillers for', default='list_of_fillers.txt')
    parser.add_argument('--onlycreate', help='Only create fillers, do not add request', action='store_true', default=False)
    parser.add_argument('--token', help='fritz token')
    args = parser.parse_args()
    return args

def is_source_on_fritz(name, token):
    url = f'https://fritz.science/api/sources/{name}'
    response = requests.get(url, headers={'Authorization': f'token {token}'})
    if response.status_code == 200:
        return True
    else:
        return False
def create_source_on_fritz(sourceDict, token):
    if 'id' not in sourceDict.keys():
        raise Exception('Source dictionary must have an id key')
    url = 'https://fritz.science/api/sources'
    response = requests.post(url, headers={'Authorization': f'token {token}'}, json=sourceDict)
    if response.status_code == 200:
        return True
    else:
        return False

def create_source_dict(name, ra, dec, group_ids=[1423]):
    if (not isinstance(ra, float)) or (not isinstance(dec, float)):
        raise Exception('RA and Dec must be floats (degrees)')
    return {'id': name, 'ra': ra, 'dec': dec, 'group_ids': group_ids}

def add_request_to_source(requestDict, token):
    url = f'https://fritz.science/api/followup_request'
    response = requests.post(url, headers={'Authorization': f'token {token}'}, json=requestDict)
    if response.status_code == 200:
        return True
    else:
        print(response.text)
        return False

def create_default_filler_request(object_id, exposure_time, observation_choice, observation_type):
    group_id = 1423
    allocation_id = 1050
    priority = 0
    start_date = Time('2023-06-01T00:00:00',format='isot')
    end_date = (start_date + 5*u.year)
    if observation_choice == 'IFU':
        observation_type = 'transient'
        payload = {'priority': priority, 'start_date': start_date.isot, 'end_date': end_date.isot,
                   'observation_type': observation_type, 'exposure_time': float(exposure_time),
                   'observation_choice': observation_choice, 'maximum_airmass': 3.0, 'too': 'N',
                   'minimum_lunar_distance': 30}
    else:
        if observation_type == 'variable':
            frame_exposure_time = 10
        payload = {'priority': priority, 'start_date': start_date.isot, 'end_date': end_date.isot,
                   'observation_type': observation_type, 'exposure_time': float(exposure_time),
                   'observation_choice': observation_choice, 'frame_exposure_time': frame_exposure_time,
                   'maximum_airmass': 3.0, 'too': 'N', 'minimum_lunar_distance': 30}
    return {'obj_id': object_id, 'target_group_ids': [group_id], 'allocation_id': allocation_id, 'status': 'submitted',\
            'payload': payload}


def main():
    args = parse_commandline()
    if not args.token:
        if os.path.exists(f'{os.getcwd()}/token.txt'):
            args.token = open(f'{os.getcwd()}/token.txt', 'r').read().strip()
        else:
            raise Exception('No token provided')

    df = pd.read_csv(args.list)
    for i in range(len(df)):
        name = df.iloc[i]['object_id'].strip()
        ra = df.iloc[i]['ra'].strip()
        dec = df.iloc[i]['dec'].strip()
        coords = SkyCoord(ra=ra, dec=dec, unit=(u.hourangle, u.deg))
        rad = coords.ra.deg
        decd = coords.dec.deg
        if not is_source_on_fritz(name, args.token):
            sourceDict = create_source_dict(name, rad, decd)
            if create_source_on_fritz(sourceDict, args.token):
                print(f'Successfully created source {name}')
            else:
                print(f'Failed to create source {name}')
        else:
            print(f'Source {name} already exists on fritz')

        if not args.onlycreate:
            exptime = df.iloc[i]['exposure_time']
            if df.iloc[i]['requester'] == 'cal':
                ob_type = 'transient'
                ob_choices = [df.iloc[i]['observation_choice']]
            elif df.iloc[i]['requester'] == 'fil':
                ob_type = 'variable'
                ob_choices = ['g', 'r', 'i', 'z']
            else:
                raise Exception('Unknown requester, not cal or fil')
            for ob_choice in ob_choices:
                requestDict = create_default_filler_request(name, exptime, ob_choice, ob_type)
                # print(requestDict)
                if add_request_to_source(requestDict, args.token):
                    print(f'Successfully added request to source {name}')
                else:
                    print(f'Failed to add request to source {name}')

if __name__ == '__main__':
    main()
