#!/usr/bin/env python

__all__ = ['quanmin_download']

from ..common import *
import json
import time

def quanmin_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    roomid = url[url.rfind("/")+1:]
    json_request_url = 'http://www.quanmin.tv/json/rooms/{}/info4.json'.format(roomid)
    content = get_html(json_request_url)
    data = json.loads(content)

    title = data["title"]
    
    if not data["play_status"]:
        raise ValueError("The live stream is not online!")
    real_url = "http://flv.quanmin.tv/live/{}.flv".format(roomid)

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_urls([real_url], title, 'flv', None, output_dir, merge = merge)

site_info = "quanmin.tv"
download = quanmin_download
download_playlist = playlist_not_supported('quanmin')
