#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor

import json
import time
from random import random
from urllib.parse import urlparse

'''
Changelog:
    1. http://tv.sohu.com/upload/swf/20150604/Main.swf
        new api
'''


class Sohu(VideoExtractor):
    name = "搜狐 (Sohu)"

    stream_types = [
        {'id': 'oriVid', 'container': 'mp4', 'video_profile': '原画'},
        {'id': 'superVid', 'container': 'mp4', 'video_profile': '超清'},
        {'id': 'highVid', 'container': 'mp4', 'video_profile': '高清'},
        {'id': 'norVid', 'container': 'mp4', 'video_profile': '标清'},
    ]

    realurls = { 'oriVid': [], 'superVid': [], 'highVid': [], 'norVid': [], 'relativeId': []}

    def real_url(host, vid, tvid, new, clipURL, ck):
        return 'http://'+host+'/?prot=9&prod=flash&pt=1&file='+clipURL+'&new='+new +'&key='+ ck+'&vid='+str(vid)+'&uid='+str(int(time.time()*1000))+'&t='+str(random())


    def get_vid_from_content(content):
        return match1(content, '\/([0-9]+)\/v\.swf') or \
                match1(content, '\&id=(\d+)')

    def parser_info(self, info, stream, lvid):
        host = info['allot']
        prot = info['prot']
        tvid = info['tvid']
        data = info['data']
        size = sum(map(int,data['clipsBytes']))
        assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
        for new, clip, ck, in zip(data['su'], data['clipsURL'], data['ck']):
            clipURL = urlparse(clip).path
            self.realurls[stream['id']].append(self.__class__.real_url(host, lvid, tvid, new, clipURL, ck))
        self.streams[stream['id']] = {'container': 'mp4', 'video_profile': stream['video_profile'], 'size' : size}


    def prepare(self, **kwargs):
        assert self.url or self.vid

        if self.url and not self.vid:
            self.vid = self.__class__.get_vid_from_content(str(get_decoded_html(self.url)))

        info = json.loads(get_decoded_html('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % self.vid))
        if info['status'] == 1:
            data = info['data']
            self.title = data['tvName']
            for stream in self.stream_types:
                lvid = data[stream['id']]
                if lvid == 0:
                    continue
                if lvid != self.vid :
                    info = json.loads(get_decoded_html('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % lvid))
                self.parser_info(info, stream, lvid)
            return
        info = json.loads(get_decoded_html('http://my.tv.sohu.com/play/videonew.do?vid=%s&referer=http://my.tv.sohu.com' % self.vid))
        if info['status'] == 1:
            data = info['data']
            self.title = data['tvName']
            for stream in self.stream_types:
                lvid = data[stream['id']]
                info = json.loads(get_decoded_html('http://my.tv.sohu.com/play/videonew.do?vid=%s&referer=http://my.tv.sohu.com' % lvid))
                self.parser_info(info, stream, lvid)
            return

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


        urls = []
        for url in self.realurls[stream_id]:
            info = json.loads(get_html(url))
            urls.append(info['url'])
        self.streams[stream_id]['src'] = urls


site = Sohu()
download = site.download_by_url
sohu_download_by_vid = site.download_by_vid
download_playlist = playlist_not_supported('sohu')
