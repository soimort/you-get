import json
import re

from ..common import get_content, playlist_not_supported, url_size
from ..extractors import VideoExtractor
from ..util import log

__all__ = ['qingting_download_by_url']


class Qingting(VideoExtractor):
    # every resource is described by its channel id and program id
    # so vid is tuple (chaanel_id, program_id)

    name = 'Qingting'
    stream_types = [
        {'id': '_default'}
    ]

    ep = 'http://i.qingting.fm/wapi/channels/{}/programs/{}'
    file_host = 'http://od.qingting.fm/{}'
    mobile_pt = r'channels\/(\d+)\/programs/(\d+)'

    def prepare(self, **kwargs):
        if self.vid is None:
            hit = re.search(self.__class__.mobile_pt, self.url)
            self.vid = (hit.group(1), hit.group(2))

        ep_url = self.__class__.ep.format(self.vid[0], self.vid[1])
        meta = json.loads(get_content(ep_url))

        if meta['code'] != 0:
            log.wtf(meta['message']['errormsg'])

        file_path = self.__class__.file_host.format(meta['data']['file_path'])
        self.title = meta['data']['name']
        duration = str(meta['data']['duration']) + 's'

        self.streams['_default'] = {'src': [file_path], 'video_profile': duration, 'container': 'm4a'}

    def extract(self, **kwargs):
        self.streams['_default']['size'] = url_size(self.streams['_default']['src'][0])


def qingting_download_by_url(url, **kwargs):
    Qingting().download_by_url(url, **kwargs)

site_info = 'Qingting'
download = qingting_download_by_url
download_playlist = playlist_not_supported('Qingting')
