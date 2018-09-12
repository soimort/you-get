#!/usr/bin/env python

__all__ = ['sohu_download']

import json
import time
from random import random
from urllib.parse import urlparse

from ..common import *

'''
Changelog:
    1. http://tv.sohu.com/upload/swf/20150604/Main.swf
        new api
'''


def real_url(host, vid, tvid, new, clipURL, ck):
    if host:
        clipURL = urlparse(clipURL).path
        url = 'http://' + host + '/?prot=9&prod=flash&pt=1&file=' + clipURL + '&new=' + new + '&key=' + ck + '&vid=' + str(vid) + '&uid=' + str(
            int(time.time() * 1000)) + '&t=' + str(random()) + '&rb=1'
        return json.loads(get_html(url))['url']
    else:
        if not clipURL.startswith('http://'):
            return 'http://' + clipURL
        return clipURL


def sohu_download(url, output_dir='.', merge=True, info_only=False, extractor_proxy=None, **kwargs):
    if re.match(r'http://share\.vrs\.sohu\.com', url):
        vid = r1('id=(\d+)', url)
    elif re.match(r'https?://my\.tv\.sohu\.com/us/\d+/(\d+)\.shtml', url):
        vid = r1(r'http://my\.tv\.sohu\.com/us/\d+/(\d+)\.shtml', url)
    else:
        html = get_html(url)
        vid = r1(r'\Wvid\s*[\:=]\s*[\'"]?(\d+)[\'"]?', html)
    assert vid

    if re.match(r'http[s]://tv.sohu.com/', url):
        if extractor_proxy:
            set_proxy(tuple(extractor_proxy.split(":")))
        info = json.loads(get_decoded_html('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % vid))
        for qtyp in ["oriVid", "superVid", "highVid", "norVid", "relativeId"]:
            if 'data' in info:
                hqvid = info['data'][qtyp]
            else:
                hqvid = info[qtyp]
            if hqvid != 0 and hqvid != vid:
                info = json.loads(get_decoded_html('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % hqvid))
                if not 'allot' in info:
                    continue
                break
        if extractor_proxy:
            unset_proxy()
        host = info['allot']
        prot = info['prot']
        tvid = info['tvid']
        urls = []
        data = info['data']
        title = data['tvName']
        size = sum(data['clipsBytes'])
        assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
        for new, clip, ck, in zip(data['su'], data['clipsURL'], data['ck']):
            urls.append(real_url(host, hqvid, tvid, new, clip, ck))
            # assert data['clipsURL'][0].endswith('.mp4')

    else:
        info = json.loads(get_decoded_html('http://my.tv.sohu.com/play/videonew.do?vid=%s&referer=http://my.tv.sohu.com' % vid))
        host = info['allot']
        prot = info['prot']
        tvid = info['tvid']
        urls = []
        data = info['data']
        title = data['tvName']
        size = sum(map(int, data['clipsBytes']))
        assert len(data['clipsURL']) == len(data['clipsBytes']) == len(data['su'])
        for new, clip, ck, in zip(data['su'], data['clipsURL'], data['ck']):
            urls.append(real_url(host, vid, tvid, new, clip, ck))

    print_info(site_info, title, 'mp4', size)
    if not info_only:
        download_urls(urls, title, 'mp4', size, output_dir, refer=url, merge=merge)


site_info = "Sohu.com"
download = sohu_download
download_playlist = playlist_not_supported('sohu')
