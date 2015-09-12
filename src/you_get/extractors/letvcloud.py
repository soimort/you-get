#!/usr/bin/env python

from ..common import *
from ..extractor import VideoExtractor
import json
import base64, hashlib, time, re

class Letvcloud(VideoExtractor):
    name = "乐视云 (Letvcloud)"

    stream_types = [
        {'id': 'yuanhua', 'container': 'mp4', 'video_profile': '原画'},
        {'id': 'super', 'container': 'mp4', 'video_profile': '超清'},
        {'id': 'high', 'container': 'mp4', 'video_profile': '高清'},
        {'id': 'low', 'container': 'mp4', 'video_profile': '标清'},
    ]

    def letvcloud_download_by_vu(self):
        #ran = float('0.' + str(random.randint(0, 9999999999999999))) # For ver 2.1
        #str2Hash = 'cfflashformatjsonran{ran}uu{uu}ver2.2vu{vu}bie^#@(%27eib58'.format(vu = vu, uu = uu, ran = ran)  #Magic!/ In ver 2.1
        vu, uu = self.vid
        argumet_dict ={'cf' : 'flash', 'format': 'json', 'ran': str(int(time.time())), 'uu': str(uu),'ver': '2.2', 'vu': str(vu), }
        sign_key = '2f9d6924b33a165a6d8b5d3d42f4f987'  #ALL YOUR BASE ARE BELONG TO US
        str2Hash = ''.join([i + argumet_dict[i] for i in sorted(argumet_dict)]) + sign_key
        sign = hashlib.md5(str2Hash.encode('utf-8')).hexdigest()
        html = get_content('http://api.letvcloud.com/gpc.php?' + '&'.join([i + '=' + argumet_dict[i] for i in argumet_dict]) + '&sign={sign}'.format(sign = sign), decoded = False)
        info = json.loads(str(html,"utf-8"))

        available_stream_type = info['data']['video_info']['media'].keys()
        for stream in self.stream_types:
            if stream['id'] in available_stream_type:
                urls = [base64.b64decode(info['data']['video_info']['media'][stream['id']]['play_url']['main_url']).decode("utf-8")]
                size = urls_size(urls)
                ext = 'mp4'
                self.streams[stream['id']] = {'container': ext, 'video_profile': stream['video_profile'], 'src': urls, 'size' : size}

    def prepare(self, **kwargs):
        assert self.url or self.vid

        if self.url and not self.vid:
            #maybe error!!
            self.vid = (vu, uu) = matchall(self.url, ["vu=([^&]+)","uu=([^&]+)"])
        _, vu = self.vid
        if 'title' in kwargs and kwargs['title']:
            self.title = kwargs['title']
        else:
            self.title = "LeTV - {}".format(vu)
        self.letvcloud_download_by_vu()

site = Letvcloud()
download = site.download_by_url
letvcloud_download_by_vid = site.download_by_vid
download_playlist = playlist_not_supported('letvcloud')
