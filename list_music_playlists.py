import os, sys
from plexapi.server import PlexServer, CONFIG
from plexapi import utils

## Edit ##
PLEX_URL = ''
PLEX_TOKEN = ''
PLEX_URL = CONFIG.data['auth'].get('server_baseurl', PLEX_URL)
PLEX_TOKEN = CONFIG.data['auth'].get('server_token', PLEX_TOKEN)

plex = PlexServer(PLEX_URL, PLEX_TOKEN)

playlists = [pl for pl in plex.playlists() if pl.isAudio]
for pl in playlists:
    print(pl.title)
