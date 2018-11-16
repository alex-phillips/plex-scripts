import os
from plexapi.server import PlexServer
from plexapi import utils

baseurl = 'https://plx.w00t.cloud'
token = 'H6gqeSNE3yGthe72x1w7'
plex = PlexServer(baseurl, token)

playlists = [pl for pl in plex.playlists()]
playlist = utils.choose('Choose Playlist', playlists, lambda pl: '%s' % pl.title)

print(len(playlist.items()))
for photo in playlist.items():
    photomediapart = photo.media[0].parts[0]
    print ('Download File: %s' % photomediapart.file)
    url = plex.url('%s?download=1' % photomediapart.key)
    utils.download(url, token, os.path.basename(photomediapart.file))
