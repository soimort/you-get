#!/usr/bin/env python

__all__ = ['lizhi_download']
import json
import datetime
from ..common import *

#
# Worked well but not perfect.
# TODO: add option --format={sd|hd}
#
def get_url(ep):
    readable = datetime.datetime.fromtimestamp(int(ep['create_time']) / 1000).strftime('%Y/%m/%d')
    return 'http://cdn5.lizhi.fm/audio/{}/{}_hd.mp3'.format(readable, ep['id'])

# radio_id: e.g. 549759 from http://www.lizhi.fm/549759/
#
# Returns a list of tuples (audio_id, title, url) for each episode
# (audio) in the radio playlist. url is the direct link to the audio
# file.
def lizhi_extract_playlist_info(radio_id):
    # /api/radio_audios API parameters:
    #
    # - s: starting episode
    # - l: count (per page)
    # - band: radio_id
    #
    # We use l=65535 for poor man's pagination (that is, no pagination
    # at all -- hope all fits on a single page).
    #
    # TODO: Use /api/radio?band={radio_id} to get number of episodes
    # (au_cnt), then handle pagination properly.
    api_url = 'http://www.lizhi.fm/api/radio_audios?s=0&l=65535&band=%s' % radio_id
    api_response = json.loads(get_content(api_url))
    return [(ep['id'], ep['name'], get_url(ep)) for ep in api_response]

def lizhi_download_audio(audio_id, title, url, output_dir='.', info_only=False):
    filetype, ext, size = url_info(url)
    print_info(site_info, title, filetype, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir)

def lizhi_download_playlist(url, output_dir='.', info_only=False, **kwargs):
    # Sample URL: http://www.lizhi.fm/549759/
    radio_id = match1(url,r'/(\d+)')
    if not radio_id:
        raise NotImplementedError('%s not supported' % url)
    for audio_id, title, url in lizhi_extract_playlist_info(radio_id):
        lizhi_download_audio(audio_id, title, url, output_dir=output_dir, info_only=info_only)

def lizhi_download(url, output_dir='.', info_only=False, **kwargs):
    # Sample URL: http://www.lizhi.fm/549759/18864883431656710/
    m = re.search(r'/(?P<radio_id>\d+)/(?P<audio_id>\d+)', url)
    if not m:
        raise NotImplementedError('%s not supported' % url)
    radio_id = m.group('radio_id')
    audio_id = m.group('audio_id')
    # Look for the audio_id among the full list of episodes
    for aid, title, url in lizhi_extract_playlist_info(radio_id):
        if aid == audio_id:
            lizhi_download_audio(audio_id, title, url, output_dir=output_dir, info_only=info_only)
            break
    else:
        raise NotImplementedError('Audio #%s not found in playlist #%s' % (audio_id, radio_id))

site_info = "lizhi.fm"
download = lizhi_download
download_playlist = lizhi_download_playlist
