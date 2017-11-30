#!/usr/bin/env python

__all__ = ['soundcloud_download', 'soundcloud_download_by_id']

from ..common import *
import json
import urllib.error

client_id = 'WKcQQdEZw7Oi01KqtHWxeVSxNyRzgT8M'

def soundcloud_download_by_id(id, title=None, output_dir='.', merge=True, info_only=False):
    assert title
    url = 'https://api.soundcloud.com/tracks/{}/{}?client_id={}'.format(id, 'stream', client_id)
    
    type, ext, size = url_info(url)
    
    print_info(site_info, title, type, size)

    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

def soundcloud_i1_api(track_id):
    url = 'https://api.soundcloud.com/i1/tracks/{}/streams?client_id={}'.format(track_id, client_id)
    return json.loads(get_content(url))['http_mp3_128_url']

def soundcloud_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    url = 'https://api.soundcloud.com/resolve.json?url={}&client_id={}'.format(url, client_id)
    metadata = get_content(url)
    info = json.loads(metadata)
    title = info["title"]
    real_url = info.get('download_url')
    if real_url is None:
        real_url = info.get('steram_url')
    if real_url is None:
        raise Exception('Cannot get media URI for {}'.format(url))
    real_url = soundcloud_i1_api(info['id'])
    mime, ext, size = url_info(real_url)
    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge=merge)

site_info = "SoundCloud.com"
download = soundcloud_download
download_playlist = playlist_not_supported('soundcloud')
