import re
import json

from ..common import get_content
from ..extractors import VideoExtractor
from ..util import log
from ..util.strings import unescape_html

__all__ = ['qq_egame_download']


class QQEgame(VideoExtractor):
    stream_types = [
        {'id': 'original', 'video_profile': '0', 'container': 'flv'},
        {'id': '900', 'video_profile': '900kb/s', 'container': 'flv'},
        {'id': '550', 'video_profile': '550kb/s', 'container': 'flv'}
    ]
    name = 'QQEgame'

    def prepare(self, **kwargs):
        page = get_content(self.url)
        server_data = re.search(r'serverData\s*=\s*({.+?});', page)
        if server_data is None:
            log.wtf('cannot find server_data')
        json_data = json.loads(server_data.group(1))
        live_info = json_data['liveInfo']['data']
        self.title = '{}_{}'.format(live_info['profileInfo']['nickName'], live_info['videoInfo']['title'])
        for exsited_stream in live_info['videoInfo']['streamInfos']:
            for s in self.__class__.stream_types:
                if re.search(r'(\d+)', s['video_profile']).group(1) == exsited_stream['bitrate']:
                    current_stream_id = s['id']
                    stream_info = dict(src=[unescape_html(exsited_stream['playUrl'])])
                    stream_info['video_profile'] = exsited_stream['desc']
                    stream_info['container'] = s['container']
                    stream_info['size'] = float('inf')
                    self.streams[current_stream_id] = stream_info


def qq_egame_download(url, **kwargs):
    QQEgame().download_by_url(url, **kwargs)
    # url dispatching has been done in qq.py
