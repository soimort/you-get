#!/usr/bin/env python

__all__ = ['panda_download']

from ..common import *
import json
import time
import requests

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
    plflag = data.get('videoinfo')['plflag'].split('_')
    status = data.get('videoinfo')['status']
    if status is not "2":
        raise ValueError("The live stream is not online! (status:%s)" % status)
    real_url = 'http://pl{}.live.panda.tv/live_panda/{}.flv'.format(plflag[1],room_key)
    counter = 0
    data2 = json.loads(data['videoinfo']['plflag_list'])
    while (requests.head(real_url, allow_redirects=True).status_code == 403 and counter < len(data2["backup"])):
        plflag = data2["backup"][counter].split('_')
        counter = counter + 1
        real_url = 'http://pl{}.live.panda.tv/live_panda/{}.flv'.format(plflag[1],room_key)
        
    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_urls([real_url], title, 'flv', None, output_dir, merge = merge)

site_info = "panda.tv"
download = panda_download
download_playlist = playlist_not_supported('panda')
