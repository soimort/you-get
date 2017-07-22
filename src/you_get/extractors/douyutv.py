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
    json_content = json.loads(content)
    data = json_content['data']
    server_status = json_content.get('error',0)
    if server_status is not 0:
        raise ValueError("Server returned error:%s" % server_status)

    room_info_url = "http://open.douyucdn.cn/api/RoomApi/room/%s" % room_id
    room_info_content = get_content(room_info_url)
    room_info_obj = json.loads(room_info_content)
    room_info_data = room_info_obj.get('data')

    title = room_info_data.get('room_name')
    show_status = room_info_data.get('room_status')
    if show_status is not "1":
        raise ValueError("The live stream is not online! (Errno:%s)" % server_status)

    real_url = data.get('hls_url')

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_url_ffmpeg(real_url, title, 'flv', None, output_dir = output_dir, merge = merge)

site_info = "douyu.com"
download = douyutv_download
download_playlist = playlist_not_supported('douyu')
