import json
import urllib.request

import pandas as pd

import auth

BASE_URL = 'https://www.thebluealliance.com/api/v3'

def _send_request(path):
    full_url = BASE_URL + path

    http_headers = {
        'X-TBA-Auth-Key': auth.tba_key,
        'User-Agent': 'Zebra Model'
    }

    req = urllib.request.Request(full_url, headers=http_headers)
    url = ''
    with urllib.request.urlopen(req) as resp:
        if resp.status == 200:
            json_response = json.loads(resp.read())
    return json_response

def get_status():
    return _send_request('/status')

def get_districts(year, df=False):
    districts = _send_request(f'/districts/{year}')
    if df:
        districts = pd.DataFrame(districts)
    return districts

def get_events_by_district(district_key, option='full', df=False):
    options = {'full': '/events',
               'simple': '/events/simple',
               'keys': '/events/keys'}
    if option.lower() not in options.keys():
        err_msg = "Data arg must be one of ['full', 'simple', 'keys']"
        raise ValueError(err_msg)
    events = _send_request(f'/district/{district_key}{options[option]}')
    if df:
        events = pd.DataFrame(events)
    return events

def get_events_by_year(year, option='full', df=False):
    options = {'full': '',
               'simple': '/simple',
               'keys': '/keys'}
    if option.lower() not in options.keys():
        err_msg = "Data arg must be one of ['full', 'simple', 'keys']"
        raise ValueError(err_msg)
    events = _send_request(f'/events/{year}{options[option]}')
    if df:
        events = pd.DataFrame(events)
    return events

def get_match_keys(event_key):
    matches = _send_request(f'/event/{event_key}/matches/keys')
    return matches

def get_zebra(match_key):
    zebra = _send_request(f'/match/{match_key}/zebra_motionworks')
    return zebra

        