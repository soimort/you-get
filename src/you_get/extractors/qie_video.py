from ..common import *
from ..extractor import VideoExtractor
from ..util.log import *

import json
import math

class QieVideo(VideoExtractor):
    name = 'QiE Video'
    vid_patt = r'"stream_name":"(\d+)"'
    title_patt = r'"title":"([^\"]+)"'
    cdn = 'http://qietv-play.wcs.8686c.com/'
    ep = 'http://api.qiecdn.com/api/v1/video/stream/{}'
    stream_types = [
        {'id':'1080p', 'video_profile':'1920x1080', 'container':'m3u8'},
        {'id':'720p', 'video_profile':'1280x720', 'container':'m3u8'},
        {'id':'480p', 'video_profile':'853x480', 'container':'m3u8'}
    ]

    def get_vid_from_url(self):
        hit = re.search(self.__class__.vid_patt, self.page)
        if hit is None:
            log.wtf('Cannot get stream_id')
        return hit.group(1)

    def get_title(self):
        hit = re.search(self.__class__.title_patt, self.page)
        if hit is None:
            return self.vid
        return hit.group(1).strip()

    def prepare(self, **kwargs):
        self.page = get_content(self.url)
        if self.vid is None:
            self.vid = self.get_vid_from_url()
        self.title = self.get_title()
        meta = json.loads(get_content(self.__class__.ep.format(self.vid)))
        if meta['code'] != 200:
            log.wtf(meta['message'])
        for video in meta['result']['videos']:
            height = video['height']
            url = self.__class__.cdn + video['key']
            stream_meta = dict(m3u8_url=url, size=0, container='m3u8')
            video_profile = '{}x{}'.format(video['width'], video['height'])
            stream_meta['video_profile'] = video_profile
            for stream_type in self.__class__.stream_types:
                if height // 10 == int(stream_type['id'][:-1]) // 10:
# width 481, 482... 489 are all 480p here
                    stream_id = stream_type['id']
                    self.streams[stream_id] = stream_meta

    def extract(self, **kwargs):
        for stream_id in self.streams:
            self.streams[stream_id]['src'], dur = general_m3u8_extractor(self.streams[stream_id]['m3u8_url'])
            self.streams[stream_id]['video_profile'] += ', Duration: {}s'.format(math.floor(dur))

def general_m3u8_extractor(url):
    dur = 0
    base_url = url[:url.rfind('/')]
    m3u8_content = get_content(url).split('\n')
    result = []
    for line in m3u8_content:
        trimmed = line.strip()
        if len(trimmed) > 0:
            if trimmed.startswith('#'):
                if trimmed.startswith('#EXTINF'):
                    t_str = re.search(r'(\d+\.\d+)', trimmed).group(1)
                    dur += float(t_str)
            else:
                if trimmed.startswith('http'):
                    result.append(trimmed)
                else:
                    result.append(base_url + '/' + trimmed)
    return result, dur 
    
site = QieVideo()
download_by_url = site.download_by_url
