#!/usr/bin/env python
# -*- coding: utf-8 -*-

from ..common import *
from ..extractor import VideoExtractor

from json import loads
from urllib.parse import urlsplit
from os.path import dirname
import re

import base64
import time
import uuid


class MGTV(VideoExtractor):
    name = "芒果 (MGTV)"

    # Last updated: 2016-11-13
    stream_types = [
        {'id': 'fhd', 'container': 'ts', 'video_profile': '蓝光'},
        {'id': 'hd', 'container': 'ts', 'video_profile': '超清'},
        {'id': 'sd', 'container': 'ts', 'video_profile': '高清'},
        {'id': 'ld', 'container': 'ts', 'video_profile': '标清'},
    ]

    id_dic = {i['video_profile']: (i['id']) for i in stream_types}

    did = str(uuid.uuid4())
    ver = '0.3.0301'
    pno = '1030'

    def tk2(self):
        return base64.urlsafe_b64encode(b'did=%s|ver=%s|pno=%s|clit=%d' % (
            self.did.encode(), self.ver.encode(), self.pno.encode(), time.time())).decode('utf-8')[::-1]

    info_endpoint = 'https://pcweb.api.mgtv.com/video/info?vid={video_id}'
    player_endpoint = 'https://pcweb.api.mgtv.com/player/video?did={did}&tk2={tk2}&video_id={video_id}'
    source_endpoint = 'https://pcweb.api.mgtv.com/player/getSource?tk2={tk2}&pm2={pm2}&video_id={video_id}'
    playlist_endpoint = 'https://pcweb.api.mgtv.com/episode/list?video_id={video_id}&page={page}&size=30'

    @staticmethod
    def get_vid_from_url(url):
        """Extracts video ID from URL.
        """
        vid = match1(url, 'https?://www.mgtv.com/(?:b|l)/\d+/(\d+).html')
        if not vid:
            vid = match1(url, 'https?://www.mgtv.com/hz/bdpz/\d+/(\d+).html')
        if not vid:
            vid = match1(url, 'https?://www.mgtv.com/s/(\d+).html')
        return vid

    # ----------------------------------------------------------------------
    def get_mgtv_real_url(self, url):
        """str->list of str
        Give you the real URLs."""
        content = loads(get_content(url))
        m3u_url = content['info']
        split = urlsplit(m3u_url)

        base_url = "{scheme}://{netloc}{path}/".format(scheme=split[0],
                                                       netloc=split[1],
                                                       path=dirname(split[2]))

        content = get_content(content['info'],
                              headers={'Referer': self.url})  # get the REAL M3U url, maybe to be changed later?
        segment_list = []
        segments_size = 0
        for i in content.split():
            if not i.startswith('#'):  # not the best way, better we use the m3u8 package
                segment_list.append(base_url + i)
            # use ext-info for fast size calculate
            elif i.startswith('#EXT-MGTV-File-SIZE:'):
                segments_size += int(i[i.rfind(':') + 1:])

        return m3u_url, segments_size, segment_list

    def download_playlist_by_url(self, url, **kwargs):
        self.url = url
        self.vid = self.get_vid_from_url(self.url)
        content_playlist = get_content(self.playlist_endpoint.format(video_id=self.vid, page=1))
        content_playlist = loads(content_playlist)
        for ep in content_playlist['data']['list']:
            self.download_by_url('https://www.mgtv.com' + ep['url'], **kwargs)
        max_page = content_playlist['data']['total_page']
        for page in range(2, max_page + 1):
            content_playlist = get_content(self.playlist_endpoint.format(video_id=self.vid, page=page))
            content_playlist = loads(content_playlist)
            for ep in content_playlist['data']['list']:
                self.download_by_url('https://www.mgtv.com' + ep['url'], **kwargs)

    def prepare(self, **kwargs):
        if self.url:
            self.vid = self.get_vid_from_url(self.url)
        content_info = get_content(self.info_endpoint.format(video_id=self.vid))
        log.d(content_info)
        content_info = loads(content_info)
        self.title = content_info['data']['info']['videoName']

        content_player = get_content(self.player_endpoint.format(did=self.did, video_id=self.vid, tk2=self.tk2()))
        log.d(content_player)
        content_player = loads(content_player)
        pm2 = content_player['data']['atc']['pm2']

        content_source = get_content(self.source_endpoint.format(video_id=self.vid, tk2=self.tk2(), pm2=pm2))
        log.d(content_source)
        content_source = loads(content_source)
        domain = content_source['data']['stream_domain'][0]

        # stream_available = [i['name'] for i in content['data']['stream']]
        stream_available = {}
        for i in content_source['data']['stream']:
            stream_available[i['name']] = i['url']

        for s in self.stream_types:
            if s['video_profile'] in stream_available.keys():
                quality_id = self.id_dic[s['video_profile']]
                url = stream_available[s['video_profile']]
                if url is None or url == '':
                    # skip invalid profile with empty url
                    continue
                url = domain + re.sub(r'(\&arange\=\d+)', '', url)  # Un-Hum
                m3u8_url, m3u8_size, segment_list_this = self.get_mgtv_real_url(url)

                stream_fileid_list = []
                for i in segment_list_this:
                    stream_fileid_list.append(os.path.basename(i).split('.')[0])

                # make pieces
                pieces = []
                for i in zip(stream_fileid_list, segment_list_this):
                    pieces.append({'fileid': i[0], 'segs': i[1], })

                    self.streams[quality_id] = {
                        'container': s['container'],
                        'video_profile': s['video_profile'],
                        'size': m3u8_size,
                        'pieces': pieces,
                        'm3u8_url': m3u8_url
                    }

                if not kwargs['info_only']:
                    self.streams[quality_id]['src'] = segment_list_this

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

    def download(self, **kwargs):

        if 'stream_id' in kwargs and kwargs['stream_id']:
            stream_id = kwargs['stream_id']
        else:
            stream_id = 'null'

        # print video info only
        if 'info_only' in kwargs and kwargs['info_only']:
            if stream_id != 'null':
                if 'index' not in kwargs:
                    self.p(stream_id)
                else:
                    self.p_i(stream_id)
            else:
                # Display all available streams
                if 'index' not in kwargs:
                    self.p([])
                else:
                    stream_id = self.streams_sorted[0]['id'] if 'id' in self.streams_sorted[0] else \
                        self.streams_sorted[0]['itag']
                    self.p_i(stream_id)

        # default to use the best quality
        if stream_id == 'null':
            stream_id = self.streams_sorted[0]['id']

        stream_info = self.streams[stream_id]

        if not kwargs['info_only']:
            if player:
                # with m3u8 format because some video player can process urls automatically (e.g. mpv)
                launch_player(player, [stream_info['m3u8_url']])
            else:
                download_urls(stream_info['src'], self.title, stream_info['container'], stream_info['size'],
                              output_dir=kwargs['output_dir'],
                              merge=kwargs.get('merge', True),
                              headers={'Referer': self.url})
                # av=stream_id in self.dash_streams)


site = MGTV()
download = site.download_by_url
download_playlist = site.download_playlist_by_url
