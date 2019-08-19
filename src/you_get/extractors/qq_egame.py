import re
import json

from ..common import *
from ..extractors import VideoExtractor
from ..util import log
from ..util.strings import unescape_html

__all__ = ['qq_egame_download']


def qq_egame_download(url,
                      output_dir='.',
                      merge=True,
                      info_only=False,
                      **kwargs):
    uid = re.search('\d\d\d+', url)
    an_url = "https://m.egame.qq.com/live?anchorid={}&".format(uid.group(0))
    page = get_content(an_url)
    server_data = re.search(r'window\.serverData\s*=\s*({.+?});', page)
    if server_data is None:
        log.wtf('Can not find window.server_data')
    json_data = json.loads(server_data.group(1))
    if json_data['anchorInfo']['data']['isLive'] == 0:
        log.wtf('Offline...')
    live_info = json_data['liveInfo']['data']
    title = '{}_{}'.format(live_info['profileInfo']['nickName'],
                           live_info['videoInfo']['title'])
    real_url = live_info['videoInfo']['streamInfos'][0]['playUrl']

    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_url_ffmpeg(
            real_url,
            title,
            'flv',
            params={},
            output_dir=output_dir,
            merge=merge)


site_info = "egame.qq.com"
download = qq_egame_download
download_playlist = playlist_not_supported('qq_egame')
