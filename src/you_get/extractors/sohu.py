#!/usr/bin/env python

__all__ = ['sohu_download']

from ..common import *

import json
import time
from random import random
from urllib.parse import urlparse

'''
Changelog:
    1. http://tv.sohu.com/upload/swf/20150604/Main.swf
        new api
'''


def real_url(fileName, key, ch):
    url = "https://data.vod.itc.cn/ip?new=" + fileName + "&num=1&key=" + key + "&ch=" + ch + "&pt=1&pg=2&prod=h5n"
    return json.loads(get_html(url))['servers'][0]['url']


def sohu_download(url, output_dir='.', merge=True, info_only=False, extractor_proxy=None, **kwargs):
    if re.match(r'http://share.vrs.sohu.com', url):
        vid = r1('id=(\d+)', url)
    else:
        html = get_html(url)
        vid = r1(r'\Wvid\s*[\:=]\s*[\'"]?(\d+)[\'"]?', html) or r1(r'bid:\'(\d+)\',', html) or r1(r'bid=(\d+)', html)
    assert vid

    if extractor_proxy:
        set_proxy(tuple(extractor_proxy.split(":")))
    info = json.loads(get_decoded_html('http://hot.vrs.sohu.com/vrs_flash.action?vid=%s' % vid))
    if info and info.get("data", ""):
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
        for fileName, key in zip(data['su'], data['ck']):
            urls.append(real_url(fileName, key, data['ch']))
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
        for fileName, key in zip(data['su'], data['ck']):
            urls.append(real_url(fileName, key, data['ch']))

    print_info(site_info, title, 'mp4', size)
    if not info_only:
        download_urls(urls, title, 'mp4', size, output_dir, refer=url, merge=merge)


site_info = "Sohu.com"
download = sohu_download
download_playlist = playlist_not_supported('sohu')
