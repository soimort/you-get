#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common import *
from ..extractor import VideoExtractor

from json import loads

class QiE(VideoExtractor):
    name = "QiE （企鹅直播）"

    # Last updated: 2015-11-24
    stream_types = [
        {'id': 'normal', 'container': 'flv', 'video_profile': '标清'},
        {'id': 'middle', 'container': 'flv', 'video_profile': '550'},
        {'id': 'middle2', 'container': 'flv', 'video_profile': '900'},
    ]
    
    id_dic = {i['video_profile']:(i['id']) for i in stream_types}
    
    api_endpoint = 'http://www.qie.tv/api/v1/room/{room_id}'

    @staticmethod
    def get_vid_from_url(url):
        """Extracts video ID from live.qq.com.
        """
        html = get_content(url)
        return match1(html, r'room_id\":(\d+)')

    def download_playlist_by_url(self, url, **kwargs):
        pass

    def prepare(self, **kwargs):
        if self.url:
            self.vid = self.get_vid_from_url(self.url)
        
        content = get_content(self.api_endpoint.format(room_id = self.vid))
        content = loads(content)
        self.title = content['data']['room_name']
        rtmp_url =  content['data']['rtmp_url']
        #stream_avalable = [i['name'] for i in content['data']['stream']]
        stream_available = {}
        stream_available['normal'] = rtmp_url + '/' + content['data']['rtmp_live']
        if len(content['data']['rtmp_multi_bitrate']) > 0:
            for k , v in content['data']['rtmp_multi_bitrate'].items():
                stream_available[k] = rtmp_url + '/' + v
        
        for s in self.stream_types:
            if s['id'] in stream_available.keys():
                quality_id = s['id']
                url = stream_available[quality_id]
                self.streams[quality_id] = {
                    'container': 'flv',
                    'video_profile': s['video_profile'],
                    'size': 0,
                    'url': url
                }

    def extract(self, **kwargs):
        for i in self.streams:
            s = self.streams[i]
            s['src'] = [s['url']]
        if 'stream_id' in kwargs and kwargs['stream_id']:
            # Extract the stream
            stream_id = kwargs['stream_id']

            if stream_id not in self.streams:
                log.e('[Error] Invalid video format.')
                log.e('Run \'-i\' command with no specific video format to view all available formats.')
                exit(2)
        else:
            # Extract stream with the best quality
            stream_id = self.streams_sorted[0]['id']
            s['src'] = [s['url']]

site = QiE()
download = site.download_by_url
download_playlist = playlist_not_supported('QiE')