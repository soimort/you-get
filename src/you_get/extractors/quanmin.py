#!/usr/bin/env python

__all__ = ['quanmin_download']

from ..common import *
import json

def quanmin_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    roomid = url.split('/')[3].split('?')[0]

    json_request_url = 'http://m.quanmin.tv/json/rooms/{}/noinfo6.json'.format(roomid)
    content = get_html(json_request_url)
    data = json.loads(content)

    title = data["title"]

    if not data["play_status"]:
        raise ValueError("The live stream is not online!")
        
    real_url = data["live"]["ws"]["flv"]["5"]["src"]

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_urls([real_url], title, 'flv', None, output_dir, merge = merge)

site_info = "quanmin.tv"
download = quanmin_download
download_playlist = playlist_not_supported('quanmin')
