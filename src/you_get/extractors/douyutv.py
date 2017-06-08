#!/usr/bin/env python

__all__ = ['douyutv_download']

from ..common import *
import json
import hashlib
import time

def douyutv_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    html = get_content(url)
    room_id_patt = r'"room_id"\s*:\s*(\d+),'
    room_id = match1(html, room_id_patt)
    if room_id == "0":
        room_id = url[url.rfind('/')+1:]

    json_request_url = "http://m.douyu.com/html5/live?roomId=%s" % room_id
    content = get_content(json_request_url)
    data = json.loads(content)['data']
    server_status = data.get('error',0)
    if server_status is not 0:
        raise ValueError("Server returned error:%s" % server_status)

    title = data.get('room_name')
    show_status = data.get('show_status')
    if show_status is not "1":
        raise ValueError("The live stream is not online! (Errno:%s)" % server_status)

    tt = int(time.time())
    sign_content = 'lapi/live/thirdPart/getPlay/%s?aid=pcclient&rate=0&time=%s9TUk5fjjUjg9qIMH3sdnh' % (room_id, tt)
    sign = hashlib.md5(sign_content.encode('ascii')).hexdigest()

    json_request_url = "http://coapi.douyucdn.cn/lapi/live/thirdPart/getPlay/%s?rate=0" % room_id
    headers = {'auth': sign, 'time': str(tt), 'aid': 'pcclient'}
    content = get_content(json_request_url, headers = headers)
    data = json.loads(content)['data']
    server_status = data.get('error',0)
    if server_status is not 0:
        raise ValueError("Server returned error:%s" % server_status)

    real_url = data.get('live_url')

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_url_ffmpeg(real_url, title, 'flv', None, output_dir = output_dir, merge = merge)

site_info = "douyu.com"
download = douyutv_download
download_playlist = playlist_not_supported('douyu')
