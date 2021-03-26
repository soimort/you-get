#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common import *
from ..extractor import VideoExtractor

class Haokan(VideoExtractor):
    name = "Haokan"

    # Haokan media encoding options, in descending quality order.
    stream_types = [
        {'id': 'sd','container': 'MP4','quality':360,'video_profile': '360p', 'desc': '标清'},
        {'id': 'hd','container': 'MP4','quality':480,'video_profile': '480p', 'desc': '高清'},
        {'id': 'sc','container': 'MP4','quality':720, 'video_profile': '720p', 'desc': '超清'},
        {'id': '1080p','container': 'MP4','quality':1080,'video_profile': '1080p', 'desc': '蓝光'},
    ]

    def extract(self, **kwargs):
        if not self.streams_sorted:
            # no stream is available
            return

        if 'stream_id' in kwargs and kwargs['stream_id']:
            # extract the stream
            stream_id = kwargs['stream_id']
            if stream_id not in self.streams and stream_id not in self.dash_streams:
                log.e('[Error] Invalid video format.')
                log.e('Run \'-i\' command with no specific video format to view all available formats.')
                exit(2)
        else:
            # extract stream with the best quality
            stream_id = self.streams_sorted[0]['id']

    def prepare(self, **kwargs):
        self.stream_qualities = {s['id']: s for s in self.stream_types}
        try:
            html_content = get_content(self.url)
        except:
            html_content = ""
        if len(html_content) < 1:
            return
        playinfo_text = match1(html_content, r'__PRELOADED_STATE__ = (.*?);')  # FIXME
        playinfo = json.loads(playinfo_text) if playinfo_text else None
        if playinfo is not None and "curVideoMeta" in playinfo:
            curVideoMeta = playinfo["curVideoMeta"]
            self.title = curVideoMeta["title"]
            for videoInfo in curVideoMeta["clarityUrl"]:
                key = videoInfo["key"]
                format_id = self.stream_qualities[key]['id']
                video_profile = self.stream_qualities[key]['video_profile']
                desc = self.stream_qualities[key]['desc']
                container = self.stream_qualities[key]['container']
                size = videoInfo['videoSize']*1024*1024
                src  = videoInfo['url']
                self.streams[format_id] = {'container': container, 'video_profile': video_profile, 'desc': desc,'size': size,'src':[src]}

site = Haokan()
download = site.download_by_url
download_playlist = playlist_not_supported("haokan")
