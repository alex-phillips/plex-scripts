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
playlist = None
if sys.argv[1]:
    for pl in playlists:
        if pl.title == sys.argv[1]:
            playlist = pl
    if playlist is None:
        print("Invalid playlist '{}'".format(sys.argv[1]))
        sys.exit()
else:
    playlist = utils.choose('Playlist to export', playlists, lambda pl: '%s' % pl.title)

for song in playlist.items():
    print(song.media[0].parts[0].file)
