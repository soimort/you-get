#!/usr/bin/env python

__all__ = ['zhanqi_download']

from ..common import *
import json
import base64
from urllib.parse import urlparse

def zhanqi_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    path = urlparse(url).path[1:]

    if not (path.startswith('videos') or path.startswith('v2/videos')): #url = "https://www.zhanqi.tv/huashan?param_s=1_0.2.0"
        path_list = path.split('/')
        room_id = path_list[1] if path_list[0] == 'topic' else path_list[0]
        zhanqi_live(room_id, merge=merge, output_dir=output_dir, info_only=info_only, **kwargs)
    else: #url = 'https://www.zhanqi.tv/videos/Lyingman/2017/01/182308.html'
        # https://www.zhanqi.tv/v2/videos/215593.html
        video_id = path.split('.')[0].split('/')[-1]
        zhanqi_video(video_id, merge=merge, output_dir=output_dir, info_only=info_only, **kwargs)

def zhanqi_live(room_id, merge=True, output_dir='.', info_only=False, **kwargs):
    api_url = "https://www.zhanqi.tv/api/static/v2.1/room/domain/{}.json".format(room_id)
    json_data = json.loads(get_content(api_url))['data']
    status = json_data['status']
    if status != '4':
        raise Exception("The live stream is not online!")

    nickname = json_data['nickname']
    title = nickname + ": " + json_data['title']
    video_levels = base64.b64decode(json_data['flashvars']['VideoLevels']).decode('utf8')
    m3u8_url = json.loads(video_levels)['streamUrl']

    print_info(site_info, title, 'm3u8', 0, m3u8_url=m3u8_url, m3u8_type='master')
    if not info_only:
        download_url_ffmpeg(m3u8_url, title, 'mp4', output_dir=output_dir, merge=merge)

def zhanqi_video(video_id, output_dir='.', info_only=False, merge=True, **kwargs):
    api_url = 'https://www.zhanqi.tv/api/static/v2.1/video/{}.json'.format(video_id)
    json_data = json.loads(get_content(api_url))['data']

    title = json_data['title']
    vid = json_data['flashvars']['VideoID']
    m3u8_url = 'http://dlvod.cdn.zhanqi.tv/' + vid
    urls = general_m3u8_extractor(m3u8_url)
    print_info(site_info, title, 'm3u8', 0)
    if not info_only:
        download_urls(urls, title, 'ts', 0, output_dir=output_dir, merge=merge, **kwargs)

site_info = "www.zhanqi.tv"
download = zhanqi_download
download_playlist = playlist_not_supported('zhanqi')
