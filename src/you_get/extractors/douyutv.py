#!/usr/bin/env python

__all__ = ['douyutv_download']

from ..common import *
from ..util.log import *
import json
import hashlib
import time
import re

def douyutv_video_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    ep = 'http://vmobile.douyu.com/video/getInfo?vid='
    patt = r'show/([0-9A-Za-z]+)'
    title_patt = r'<h1>(.+?)</h1>'

    hit = re.search(patt, url)
    if hit is None:
        log.wtf('Unknown url pattern')
    vid = hit.group(1)

    page = get_content(url)
    hit = re.search(title_patt, page)
    if hit is None:
        title = vid
    else:
        title = hit.group(1)

    meta = json.loads(get_content(ep + vid))
    if meta['error'] != 0:
        log.wtf('Error from API server')
    m3u8_url = meta['data']['video_url']
    print_info('Douyu Video', title, 'm3u8', 0, m3u8_url=m3u8_url)
    if not info_only:
        urls = general_m3u8_extractor(m3u8_url)
        download_urls(urls, title, 'ts', 0, output_dir=output_dir, merge=merge, **kwargs)

def douyutv_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if 'v.douyu.com/show/' in url:
        douyutv_video_download(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
        return

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
