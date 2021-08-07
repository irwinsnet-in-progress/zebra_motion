import sys

import tba
import zebra


# def test_download_keys():
#     year = 2020
#     event_keys = tba.get_events_by_year(year, option='keys')
#     assert event_keys[0][:4] == '2020'
#     assert len(event_keys) == 196

def test_zebra():
    zebra.path_data(2020)