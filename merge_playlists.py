#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Build playlist from popular tracks.
optional arguments:
  -h, --help           show this help message and exit
  --name []            Name your playlist
  --libraries  [ ...]  Space separated list of case sensitive names to process. Allowed names are:
                       (choices: ALL MUSIC LIBRARIES)*
  --artists  [ ...]    Space separated list of case sensitive names to process. Allowed names are:
                       (choices: ALL ARTIST NAMES)
  --tracks []          Specify the track length you would like the playlist.
  --random []          Randomly select N artists.
* LIBRARY_EXCLUDE are excluded from libraries choice.
"""


import requests
from plexapi.server import PlexServer, CONFIG
import argparse
import random

# Edit
PLEX_URL = ''
PLEX_TOKEN = ''
PLEX_URL = CONFIG.data['auth'].get('server_baseurl', PLEX_URL)
PLEX_TOKEN = CONFIG.data['auth'].get('server_token', PLEX_TOKEN)

LIBRARY_EXCLUDE = ['Audio Books', 'Podcasts', 'Soundtracks']
DEFAULT_NAME = 'All Playlists'

# /Edit

sess = requests.Session()
# Ignore verifying the SSL certificate
sess.verify = False  # '/path/to/certfile'
# If verify is set to a path to a directory,
# the directory must have been processed using the c_rehash utility supplied
# with OpenSSL.
if sess.verify is False:
    # Disable the warning that the request is insecure, we know that...
    import urllib3

    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

plex = PlexServer(PLEX_URL, PLEX_TOKEN, session=sess)
playlists = [pl for pl in plex.playlists() if pl.isAudio]


def fetch(path):
    url = PLEX_URL

    header = {'Accept': 'application/json'}
    params = {'X-Plex-Token': PLEX_TOKEN,
              'includePopularLeaves': '1'
              }

    r = requests.get(url + path, headers=header, params=params, verify=False)
    return r.json()['MediaContainer']['Metadata'][0]['PopularLeaves']['Metadata']


def build_tracks(music_lst):
    ratingKey_lst = []
    track_lst = []

    for artist in music_lst:
        try:
            ratingKey_lst += fetch('/library/metadata/{}'.format(artist.ratingKey))
            for tracks in ratingKey_lst:
                track_lst.append(plex.fetchItem(int(tracks['ratingKey'])))
        except KeyError as e:
            print('Artist: {} does not have any popular tracks listed.'.format(artist.title))
            print('Error: {}'.format(e))

    return track_lst


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Merge all playlists into one playlist",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--name', nargs='?', default=DEFAULT_NAME, metavar='',
                        help='Name your playlist')
    parser.add_argument('--exclude', nargs='?', default='', metavar='',
                        help='Exclude playlists')

    opts = parser.parse_args()

    excludes = opts.exclude.split(',')
    items = []
    merged_playlist = None

    for playlist in playlists:
        if playlist.title == opts.name:
            merged_playlist = playlist
            continue

        if playlist.title in excludes:
            continue

        items = items + playlist.items()

    if merged_playlist is None:
        merged_playlist = plex.createPlaylist(opts.name, items[:1])

    # remove existing items first
    for playlist_item in merged_playlist.items():
        merged_playlist.removeItem(playlist_item)

    while len(items) > 0:
        merged_playlist.addItems(items[:100])
        items = items[100:]
