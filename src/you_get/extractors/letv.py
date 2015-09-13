#!/usr/bin/env python

import json
import random
import base64, time, re

from ..common import *
from ..extractor import VideoExtractor

def calcTimeKey(t):
    ror = lambda val, r_bits, : ((val & (2**32-1)) >> r_bits%32) |  (val << (32-(r_bits%32)) & (2**32-1))
    return ror(ror(t,773625421%13)^773625421,773625421%17)

def decode(data):
    version = data[0:5]
    if version.lower() == b'vc_01':
        #get real m3u8
        loc2 = data[5:]
        length = len(loc2)
        loc4 = [0]*(2*length)
        for i in range(length):
            loc4[2*i] = loc2[i] >> 4
            loc4[2*i+1]= loc2[i] & 15;
        loc6 = loc4[len(loc4)-11:]+loc4[:len(loc4)-11]
        loc7 = [0]*length
        for i in range(length):
            loc7[i] = (loc6[2 * i] << 4) +loc6[2*i+1]
        return ''.join([chr(i) for i in loc7])
    else:
        # directly return
        return data

class Letv(VideoExtractor):
    name = "乐视 (Letv)"

    stream_types = [
        {'id': '1080p', 'container': 'mp4', 'video_profile': '1080p'},
        {'id': '1300', 'container': 'mp4', 'video_profile': '超清'},
        {'id': '1000', 'container': 'mp4', 'video_profile': '高清'},
        {'id': '720p', 'container': 'mp4', 'video_profile': '标清'},
        {'id': '350', 'container': 'mp4', 'video_profile': '流畅'},
    ]

    def prepare(self, **kwargs):
        assert self.url or self.vid

        if self.vid:
            self.url = "http://www.letv.com/ptv/vplay/{}.html".format(self.vid)
        html = get_content(self.url)
        if not self.vid:
            self.vid = match1(self.url, r'http://www.letv.com/ptv/vplay/(\d+).html')
        if not self.vid:
           #self embed
           vids = matchall(html, ['vid="(\d+)"'])
           for v in vids:
               self.download_by_vid(v, **kwargs)

        #normal process
        self.title = match1(html,r'name="irTitle" content="(.*?)"')
        info_url = 'http://api.letv.com/mms/out/video/playJson?id={}&platid=1&splatid=101&format=1&tkey={}&domain=www.letv.com'.format(self.vid, calcTimeKey(int(time.time())))
        r = get_content(info_url, decoded=False)
        info=json.loads(str(r,"utf-8"))
        support_stream_id = info["playurl"]["dispatch"].keys()
        for stream in self.stream_types:
            if stream['id'] in support_stream_id:
                s_url =info["playurl"]["domain"][0]+info["playurl"]["dispatch"][stream['id']][0]
                ext = info["playurl"]["dispatch"][stream['id']][1].split('.')[-1]
                s_url+="&ctv=pc&m3v=1&termid=1&format=1&hwtype=un&ostype=Linux&tag=letv&sign=letv&expect=3&tn={}&pay=0&iscpn=f9051&rateid={}".format(random.random(),stream['id'])
                r2=get_content(s_url,decoded=False)
                info2=json.loads(str(r2,"utf-8"))

                # hold on ! more things to do
                # to decode m3u8 (encoded)
                m3u8 = get_content(info2["location"],decoded=False)
                m3u8_list = decode(m3u8)
                urls = re.findall(r'^[^#][^\r]*',m3u8_list,re.MULTILINE)
                self.streams[stream['id']] = {'container': ext, 'video_profile': stream['video_profile'], 'src': urls, 'size' : 0}

    def extract(self, **kwargs):
        if 'info_only' in kwargs and kwargs['info_only']:
            for stream_id in self.streams.keys():
                size = 0
                for i in self.streams[stream_id]['src']:
                    _, _, tmp = url_info(i)
                    size += tmp
                stream['size'] = size
        return
        #ignore video size in download/play mode, for preformence issue
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

        size = 0
        for i in self.streams[stream_id]['src']:
             _, _, tmp = url_info(i)
             size += tmp
             self.streams[stream_id]['size'] = size

    def download_playlist_by_url(self, url, **kwargs):
        self.url = url
        html = get_content(self.url)

        vids = matchall(html, ['vid="(\d+)"'])
        for v in vids:
            self.download_by_vid(v, **kwargs)


def letvcloud_download_by_vu(vu, uu, title=None, output_dir='.', merge=True, info_only=False, **kwargs):
    from .letvcloud import letvcloud_download_by_vid
    letvcloud_download_by_vid((vu, uu), title=title, output_dir=output_dir, merge=merge, info_only=info_only,**kwargs)

site = Letv()
download = site.download_by_url
letv_download_by_vid = site.download_by_vid
download_playlist = site.download_playlist_by_url
