import json
import urllib.error

import tba

def event_keys(year):
    print()
    print('Downloading events for', year)
    event_keys = tba.get_events_by_district('2020pnw', option='keys')
    for event_key in event_keys:
        print('Processing event:', event_key)
        yield event_key


def match_path_data(year):
    for event_key in event_keys(year):
        match_keys = tba.get_match_keys(event_key)
        for match_key in match_keys:
            try:
                zdata = tba.get_zebra(match_key)
                score_data = tba.get_match_scores(match_key)
            except urllib.error.HTTPError:
                yield event_key, match_key, None, None,
                break
            yield event_key, match_key, zdata, score_data


def path_data(year):
    with open('zebra.jsonl', 'wt') as zfile:
        for event_key, match_key, zdata, score_data in match_path_data(year):
            match_data = {'event': event_key,
                          'match': match_key,
                          'zebra': zdata,
                          'score': score_data}
            zfile.write(json.dumps(match_data) + '\n')

