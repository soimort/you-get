#!/usr/bin/env python

__all__ = ['zhanqi_download']

from ..common import *
import json

def zhanqi_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    host_name = url.split('/')[2]
    first_folder_path = url.split('/')[3].split('?')[0]

    if first_folder_path != 'videos': #url = "https://www.zhanqi.tv/huashan?param_s=1_0.2.0"
        if first_folder_path == 'topic': #https://www.zhanqi.tv/topic/lyingman
            first_folder_path = url.split('/')[4].split('?')[0]
        api_url = "https://www.zhanqi.tv/api/static/v2.1/room/domain/" + first_folder_path + ".json"
        api_json = json.loads(get_html(api_url))
        data = api_json['data']
        status = data['status']
        if status != '4':
            raise ValueError ("The live stream is not online!")

        nickname = data['nickname']
        title = nickname + ": " + data['title']

        roomid = data['id']
        videoId = data['videoId']
        jump_url = "http://wshdl.load.cdn.zhanqi.tv/zqlive/" + videoId + ".flv?get_url=1"
        jump_url = jump_url.strip('\r\n')

        real_url = get_html(jump_url)
        real_url = real_url.strip('\r\n')
        site_info = "www.zhanqi.tv"

        print_info(site_info, title, 'flv', float('inf'))
        if not info_only:
            download_url_ffmpeg(real_url, title, 'flv', {}, output_dir = output_dir, merge = merge)

    else: #url = 'https://www.zhanqi.tv/videos/Lyingman/2017/01/182308.html'
        video_id = url.split('/')[-1].split('?')[0].split('.')[0]
        assert video_id
        api_url = "https://www.zhanqi.tv/api/static/v2.1/video/" + video_id + ".json"
        api_json = json.loads(get_html(api_url))
        data = api_json['data']

        title = data['title']

        video_url_id = data['flashvars']['VideoID']
        real_url = "http://dlvod.cdn.zhanqi.tv/" + video_url_id
        site_info = "www.zhanqi.tv/videos"

        print_info(site_info, title, 'flv', float('inf'))
        if not info_only:
            download_url_ffmpeg(real_url, title, 'flv', {}, output_dir = output_dir, merge = merge)

download = zhanqi_download
download_playlist = playlist_not_supported('zhanqi')