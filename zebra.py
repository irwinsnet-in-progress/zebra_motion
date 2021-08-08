"""Tools for analyzing Zebra motion capture data from FRC Competitions.
"""

import argparse
import copy
import json
import urllib.error

import tba

def setup_parser():
    """Setup module for command-line use"""
    desc = (
        'Tools for obtaining and analyzing Zebra motion capture data '
        'collected at FIRST Robotic Competition (FRC) events.')
    parser = argparse.ArgumentParser(description=desc)
    subparsers = parser.add_subparsers()
    download_subparser = subparsers.add_parser(
        'download',
        description='Download match data from TBA')
    download_subparser.add_argument(
        'key', help='TBA district key or 4-digit year')
    download_subparser.add_argument(
        'file', help='Match data will be saved to this file.')
    download_subparser.set_defaults(func=download_data)
    return parser


def download_data(key, file):
    """Downloads motion capture data and match scores from TBA."""

    def _event_keys():
        print()
        print('Downloading events for:', key)
        event_keys = tba.get_events(key, option='keys')
        for event_key in event_keys:
            print('Processing event:', event_key)
            yield event_key

    def _match_path_data():
        for event_key in _event_keys():
            match_keys = tba.get_match_keys(event_key)
            for match_key in match_keys:
                try:
                    zdata = tba.get_zebra(match_key)
                    score_data = tba.get_match_scores(match_key)
                except urllib.error.HTTPError:
                    yield event_key, match_key, None, None,
                    break
                yield event_key, match_key, zdata, score_data

    with open(file, 'wt') as zfile:
        for event_key, match_key, zdata, score_data in _match_path_data():
            match_data = {'event': event_key,
                          'match': match_key,
                          'zebra': zdata,
                          'score': score_data}
            zfile.write(json.dumps(match_data) + '\n')


if __name__ == '__main__':
    parser = setup_parser()
    args = parser.parse_args()
    subcommand = args.func
    del args.func
    subcommand(**vars(args))
