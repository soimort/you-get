#!/usr/bin/env python

__all__ = ['douyutv_download']

from ..common import *
from ..util.log import *
import json
import hashlib
import time
import re

headers = {
        'user-agent': 'Mozilla/5.0 (iPad; CPU OS 8_1_3 like Mac OS X) AppleWebKit/600.1.4 (KHTML, like Gecko) Version/8.0 Mobile/12B466 Safari/600.1.4'
    }

def douyutv_video_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    ep = 'http://vmobile.douyu.com/video/getInfo?vid='
    patt = r'show/([0-9A-Za-z]+)'
    title_patt = r'<h1>(.+?)</h1>'

    hit = re.search(patt, url)
    if hit is None:
        log.wtf('Unknown url pattern')
    vid = hit.group(1)

    page = get_content(url, headers=headers)
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


def douyutv_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    if 'v.douyu.com/show/' in url:
        douyutv_video_download(url, output_dir=output_dir, merge=merge, info_only=info_only, **kwargs)
        return

    url = re.sub(r'.*douyu.com','https://m.douyu.com/room', url)
    html = get_content(url, headers)
    room_id_patt = r'"rid"\s*:\s*(\d+),'
    room_id = match1(html, room_id_patt)
    if room_id == "0":
        room_id = url[url.rfind('/') + 1:]

    api_url = "http://www.douyutv.com/api/v1/"
    args = "room/%s?aid=wp&client_sys=wp&time=%d" % (room_id, int(time.time()))
    auth_md5 = (args + "zNzMV1y4EMxOHS6I5WKm").encode("utf-8")
    auth_str = hashlib.md5(auth_md5).hexdigest()
    json_request_url = "%s%s&auth=%s" % (api_url, args, auth_str)

    content = get_content(json_request_url, headers)
    json_content = json.loads(content)
    data = json_content['data']
    server_status = json_content.get('error', 0)
    if server_status != 0:
        raise ValueError("Server returned error:%s" % server_status)

    title = data.get('room_name')
    show_status = data.get('show_status')
    if show_status != "1":
        raise ValueError("The live stream is not online! (Errno:%s)" % server_status)

    real_url = data.get('rtmp_url') + '/' + data.get('rtmp_live')

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_url_ffmpeg(real_url, title, 'flv', params={}, output_dir=output_dir, merge=merge)


site_info = "douyu.com"
download = douyutv_download
download_playlist = playlist_not_supported('douyu')
