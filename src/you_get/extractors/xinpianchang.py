#!/usr/bin/env python

import re
import json
from ..extractor import VideoExtractor
from ..common import get_content, playlist_not_supported


class Xinpianchang(VideoExtractor):
    name = 'xinpianchang'
    stream_types = [
        {'id': '4K', 'quality': '超清 4K', 'video_profile': 'mp4-4K'},
        {'id': '2K', 'quality': '超清 2K', 'video_profile': 'mp4-2K'},
        {'id': '1080', 'quality': '高清 1080P', 'video_profile': 'mp4-FHD'},
        {'id': '720', 'quality': '高清 720P', 'video_profile': 'mp4-HD'},
        {'id': '540', 'quality': '清晰 540P', 'video_profile': 'mp4-SD'},
        {'id': '360', 'quality': '流畅 360P', 'video_profile': 'mp4-LD'}
    ]

    def prepare(self, **kwargs):
        # find key
        page_content = get_content(self.url)
        match_rule = r"vid = \"(.+?)\";"
        key = re.findall(match_rule, page_content)[0]

        # get videos info
        video_url = 'https://openapi-vtom.vmovier.com/v3/video/' + key + '?expand=resource'
        data = json.loads(get_content(video_url))
        self.title = data["data"]["video"]["title"]
        video_info = data["data"]["resource"]["progressive"]

        # set streams dict
        for video in video_info:
            url = video["https_url"]
            size = video["filesize"]
            profile = video["profile_code"]
            stype = [st for st in self.__class__.stream_types if st['video_profile'] == profile][0]

            stream_data = dict(src=[url], size=size, container='mp4', quality=stype['quality'])
            self.streams[stype['id']] = stream_data


download = Xinpianchang().download_by_url
download_playlist = playlist_not_supported('xinpianchang')
