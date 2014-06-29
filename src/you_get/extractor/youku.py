#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common import *

class Youku(VideoExtractor):
    name = "优酷 (Youku)"

    stream_types = [
        {'id': 'hd3', 'container': 'flv', 'video_profile': '1080P'},
        {'id': 'hd2', 'container': 'flv', 'video_profile': '超清'},
        {'id': 'mp4', 'container': 'mp4', 'video_profile': '高清'},
        {'id': 'flvhd', 'container': 'flv', 'video_profile': '高清'},
        {'id': 'flv', 'container': 'flv', 'video_profile': '标清'},
        {'id': '3gphd', 'container': '3gp', 'video_profile': '高清（3GP）'},
    ]

    def __init__(self, *args):
        super().__init__(args)

    def get_vid_from_url(url):
        """Extracts video ID from URL.
        """
        patterns = [
            'youku.com/v_show/id_([\w=]+)',
            'player.youku.com/player.php/sid/([\w=]+)/v.swf',
            'loader\.swf\?VideoIDS=([\w=]+)',
        ]
        matches = match1(url, *patterns)
        if matches:
            return matches[0]
        else:
            return None

    def parse_m3u8(m3u8):
        return re.findall(r'(http://[^?]+)\?ts_start=0', m3u8)

    def prepare(self, **kwargs):
        assert self.url or self.vid
        if self.url and not self.vid:
            self.vid = __class__.get_vid_from_url(self.url)

        meta = json.loads(get_html('http://v.youku.com/player/getPlayList/VideoIDS/%s' % self.vid))
        if not meta['data']:
            log.e('[Failed] Video not found.')
            exit(3)
        metadata0 = meta['data'][0]

        self.title = metadata0['title']

        for stream_type in self.stream_types:
            if stream_type['id'] in metadata0['streamsizes']:
                stream_id = stream_type['id']
                stream_size = int(metadata0['streamsizes'][stream_id])
                self.streams[stream_id] = {'container': stream_type['container'], 'video_profile': stream_type['video_profile'], 'size': stream_size}

        if not self.streams:
            for stream_type in self.stream_types:
                if stream_type['id'] in metadata0['streamtypes_o']:
                    stream_id = stream_type['id']
                    self.streams[stream_id] = {'container': stream_type['container'], 'video_profile': stream_type['video_profile']}

    def extract(self, **kwargs):
        if 'stream_id' in kwargs and kwargs['stream_id']:
            # Extract the stream
            stream_id = kwargs['stream_id']

            if stream_id not in self.streams:
                log.e('[Failed] Invalid video format.')
                log.e('Use without specifying any video format to check all available formats.')
                exit(2)
        else:
            # Extract stream with the best quality
            stream_id = self.streams_sorted[0]['id']

        m3u8_url = "http://v.youku.com/player/getM3U8/vid/{vid}/type/{stream_id}/video.m3u8".format(vid=self.vid, stream_id=stream_id)
        m3u8 = get_html(m3u8_url)
        if not m3u8:
            log.w('[Warning] This video can only be streamed within Mainland China!')
            log.w('Use \'-y\' to specify a proxy server for extracting stream data.\n')

        self.streams[stream_id]['src'] = __class__.parse_m3u8(m3u8)

site = Youku()
download = site.download_by_url
download_playlist = playlist_not_supported('youku')

youku_download_by_vid = site.download_by_vid
# Used by: acfun.py bilibili.py miomio.py tudou.py
