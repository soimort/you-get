#!/usr/bin/env python

__all__ = ['douyutv_download']

from ..common import *
import json
import hashlib
import time
import random
import string
import requests

def douyutv_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    room_id = url[url.rfind('/')+1:]

    json_request_url = "http://m.douyu.com/html5/live?roomId=%s" % room_id
    content = get_html(json_request_url)
    data = json.loads(content)['data']
    server_status = data.get('error',0)
    if server_status is not 0:
        raise ValueError("Server returned error:%s" % server_status)

    title = data.get('room_name')
    show_status = data.get('show_status')
    if show_status is not "1":
        raise ValueError("The live stream is not online! (Errno:%s)" % server_status)

    tt = int(time.time() / 60)
    did = ''.join([random.choice(string.ascii_uppercase + string.digits) for n in range(32)])
    sign = hashlib.md5((room_id + did + 'A12Svb&%1UUmf@hC' + "%d" % tt).encode("utf-8")).hexdigest()
    json_request_url = "http://www.douyu.com/lapi/live/getPlay/%s" % room_id

    payload = {'cdn': 'ws', 'rate': '0', 'tt': tt, 'did': did, 'sign': sign}
    r = requests.post(json_request_url, data=payload)
    content = r.json()
    data = content['data']

    server_status = data.get('error',0)
    if server_status is not 0:
        raise ValueError("Server returned error:%s" % server_status)

    real_url = data.get('rtmp_url')+'/'+data.get('rtmp_live')

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_url_ffmpeg(real_url, title, 'flv', None, output_dir, merge = merge)

site_info = "douyu.com"
download = douyutv_download
download_playlist = playlist_not_supported('douyu')
