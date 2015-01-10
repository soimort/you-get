#!/usr/bin/env python

__all__ = ['soundcloud_download', 'soundcloud_download_by_id']

from ..common import *

def soundcloud_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    assert title
    
    #if info["downloadable"]:
    #   url = 'https://api.soundcloud.com/tracks/' + id + '/download?client_id=b45b1aa10f1ac2941910a7f0d10f8e28'
    url = 'https://api.soundcloud.com/tracks/' + id + '/stream?client_id=02gUJC0hH2ct1EGOcYXQIzRFU91c72Ea'
    assert url
    type, ext, size = url_info(url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

def soundcloud_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    metadata = get_html('https://api.soundcloud.com/resolve.json?url=' + url + '&client_id=02gUJC0hH2ct1EGOcYXQIzRFU91c72Ea')
    import json
    info = json.loads(metadata)
    title = info["title"]
    id = str(info["id"])
    
    soundcloud_download_by_id(id, title, output_dir, merge = merge, info_only = info_only)

site_info = "SoundCloud.com"
download = soundcloud_download
download_playlist = playlist_not_supported('soundcloud')
