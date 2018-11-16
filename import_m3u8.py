import os, sys
from plexapi.server import PlexServer, CONFIG
from plexapi import utils

## Edit ##
PLEX_URL = ''
PLEX_TOKEN = ''
PLEX_URL = CONFIG.data['auth'].get('server_baseurl', PLEX_URL)
PLEX_TOKEN = CONFIG.data['auth'].get('server_token', PLEX_TOKEN)

if len(sys.argv) != 2:
    print("Please specify an m3u8 playlist file")
    quit()

plex = PlexServer(PLEX_URL, PLEX_TOKEN)

playlists = [pl for pl in plex.playlists() if pl.isAudio]
playlist = utils.choose('Add to playlist', playlists, lambda pl: '%s' % pl.title)

# Choose which music library to pull songs from
sections = [ _ for _ in plex.library.sections() if _.type in {'artist'} ]
if not sections:
    print('No available sections.')
    sys.exit()

section = utils.choose('Select library', sections, 'title')

with open(sys.argv[1]) as f:
    files = f.read().splitlines()

print("Fetching library tracks. This could take a while...")
for media in section.searchTracks():
    mediapath = media.media[0].parts[0].file
    if mediapath in files:
        print("{} - {}".format(playlist.title, mediapath))
        playlist.addItems([media])

print("Done.")
