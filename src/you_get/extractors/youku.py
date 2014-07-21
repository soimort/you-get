#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common import *
from ..extractor import VideoExtractor

class Youku(VideoExtractor):
    name = "优酷 (Youku)"

    stream_types = [
        # FIXME: Does not work for 1080P
        # {'id': 'hd3', 'container': 'flv', 'video_profile': '1080P'},
        {'id': 'hd2', 'container': 'flv', 'video_profile': '超清'},
        {'id': 'mp4', 'container': 'mp4', 'video_profile': '高清'},
        {'id': 'flvhd', 'container': 'flv', 'video_profile': '高清'},
        {'id': 'flv', 'container': 'flv', 'video_profile': '标清'},
        {'id': '3gphd', 'container': '3gp', 'video_profile': '高清（3GP）'},
    ]

    def parse_m3u8(m3u8):
        return re.findall(r'(http://[^?]+)\?ts_start=0', m3u8)

    def get_vid_from_url(url):
        """Extracts video ID from URL.
        """
        return match1(url, r'youku\.com/v_show/id_([\w=]+)') or \
          match1(url, r'player\.youku\.com/player\.php/sid/([\w=]+)/v\.swf') or \
          match1(url, r'loader\.swf\?VideoIDS=([\w=]+)')

    def get_playlist_id_from_url(url):
        """Extracts playlist ID from URL.
        """
        return match1(url, r'youku\.com/playlist_show/id_([\w=]+)')

    def download_playlist_by_url(self, url, **kwargs):
        self.url = url

        playlist_id = __class__.get_playlist_id_from_url(self.url)
        if playlist_id is None:
            log.wtf('[Failed] Unsupported URL pattern.')

        video_page = get_content('http://www.youku.com/playlist_show/id_%s' % playlist_id)
        videos = set(re.findall(r'href="(http://v\.youku\.com/[^?"]+)', video_page))
        self.title = re.search(r'<meta name="title" content="([^"]+)"', video_page).group(1)
        self.p_playlist()
        for video in videos:
            index = parse_query_param(video, 'f')
            __class__().download_by_url(video, index=index, **kwargs)

    def prepare(self, **kwargs):
        assert self.url or self.vid

        if self.url and not self.vid:
            self.vid = __class__.get_vid_from_url(self.url)

            if self.vid is None:
                self.download_playlist_by_url(self.url, **kwargs)
                exit(0)

        meta = json.loads(get_html('http://v.youku.com/player/getPlayList/VideoIDS/%s' % self.vid))
        if not meta['data']:
            log.wtf('[Failed] Video not found.')
        metadata0 = meta['data'][0]

        self.title = metadata0['title']

        if 'dvd' in metadata0 and 'audiolang' in metadata0['dvd']:
            self.audiolang = metadata0['dvd']['audiolang']
            for i in self.audiolang:
                i['url'] = 'http://v.youku.com/v_show/id_{}'.format(i['vid'])

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
                log.e('[Error] Invalid video format.')
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
download_playlist = site.download_playlist_by_url

youku_download_by_vid = site.download_by_vid
# Used by: acfun.py bilibili.py miomio.py tudou.py
