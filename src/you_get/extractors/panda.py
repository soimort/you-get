#!/usr/bin/env python

__all__ = ['panda_download']

from ..common import *
import json
import time

def panda_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    roomid = url[url.rfind('/')+1:]
    json_request_url = 'http://www.panda.tv/api_room?roomid={}&pub_key=&_={}'.format(roomid, int(time.time()))
    content = get_html(json_request_url)
    errno = json.loads(content)['errno']
    errmsg = json.loads(content)['errmsg']
    if errno:
        raise ValueError("Errno : {}, Errmsg : {}".format(errno, errmsg))

    data = json.loads(content)['data']
    title = data.get('roominfo')['name']
    room_key = data.get('videoinfo')['room_key']
    status = data.get('videoinfo')['status']
    if status is not "2":
        raise ValueError("The live stream is not online! (status:%s)" % status)
    real_url = 'http://pl3.live.panda.tv/live_panda/{}.flv'.format(room_key)

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_urls([real_url], title, 'flv', None, output_dir, merge = merge)

site_info = "panda.tv"
download = panda_download
download_playlist = playlist_not_supported('panda')
