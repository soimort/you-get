#!/usr/bin/env python

__all__ = ['hunan_download']

from ..common import *
from ..extractor import VideoExtractor
from random import randint
import json
import re

class Hunantv(VideoExtractor):
    name = "芒果TV (HunanTV)"

    stream_types = [
        {'id': '超清', 'container': 'fhv', 'video_profile': '超清'},
        {'id': '高清', 'container': 'fhv', 'video_profile': '高清'},
        {'id': '标清', 'container': 'fhv', 'video_profile': '标清'},
    ]

    def get_vid_from_url(url):
        """Extracts video ID from URL.
        """
        return match1(url, "/([0-9]+).html")


    def prepare(self, **kwargs):
        assert self.url or self.vid

        if self.url and not self.vid:
            self.vid = self.__class__.get_vid_from_url(self.url)

        rn = randint(0, 99999999)
        api_url = 'http://v.api.hunantv.com/player/video?video_id={}&random={}'.format(self.vid,rn)
        meta = json.loads(get_html(api_url))
        if meta['status'] != 200:
            log.wtf('[failed] status: {}, msg: {}'.format(meta['status'],meta['msg']))
        if not meta['data']:
            log.wtf('[Failed] Video not found.')
        data = meta['data']

        info = data['info']
        self.title = info['title']

        self.lstreams = data['stream']

        for lstream in self.lstreams:
               self.streams[lstream['name']] = {'container': 'fhv', 'video_profile': lstream['name'], 'size' : 0}

    def extract(self, **kwargs):
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

        for lstream in self.lstreams:
            if stream_id == lstream['name']:
                meta = ''
                while True:
                    rn = randint(0, 99999999)
                    meta = json.loads(get_html("{}&random={}".format((lstream['url']),rn)))
                    if meta['status'] == 'ok':
                        if meta['info'].startswith('http://pcfastvideo.imgo.tv/'):
                            break
                self.streams[stream_id]['src'] = [meta['info']]

site = Hunantv()
download = site.download_by_url
hunan_download_by_vid = site.download_by_vid
download_playlist = playlist_not_supported('hunantv')
