#!/usr/bin/env python

__all__ = ['yizhibo_download']

from ..common import *
import json
import time

def yizhibo_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    video_id = url[url.rfind('/')+1:].split(".")[0]
    json_request_url = 'http://www.yizhibo.com/live/h5api/get_basic_live_info?scid={}'.format(video_id)
    content = get_html(json_request_url)
    error = json.loads(content)['result']
    if (error != 1):
        raise ValueError("Error : {}".format(error))

    data = json.loads(content)#['data']
    title = data.get('data')['live_title']
    if (title == ''):
        title = data.get('data')['nickname']
    real_url = data.get('data')['play_url']

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_url_ffmpeg(real_url, title, 'flv', None, output_dir, merge = merge)

site_info = "yizhibo.com"
download = yizhibo_download
download_playlist = playlist_not_supported('yizhibo')
