#!/usr/bin/env python

__all__ = ['douyutv_download']

from ..common import *
import json

def douyutv_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    room_id = url[url.rfind('/')+1:]

    content = get_html("http://www.douyutv.com/api/client/room/"+room_id)
    data = json.loads(content)['data']

    title = data.get('room_name')
    real_url = data.get('rtmp_url')+'/'+data.get('rtmp_live')

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_urls([real_url], title, 'flv', None, output_dir, merge = merge)

site_info = "douyutv.com"
download = douyutv_download
download_playlist = playlist_not_supported('douyutv')
