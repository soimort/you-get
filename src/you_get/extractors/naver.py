#!/usr/bin/env python

import urllib.request
import urllib.parse
import json
import re

from ..util import log
from ..common import get_content, download_urls, print_info, playlist_not_supported, url_size
from .universal import *

__all__ = ['naver_download_by_url']


def naver_download_by_url(url, output_dir='.', merge=True, info_only=False, **kwargs):
    ep = 'https://apis.naver.com/rmcnmv/rmcnmv/vod/play/v2.0/{}?key={}'
    page = get_content(url)
    try:
        vid = re.search(r"\"videoId\"\s*:\s*\"(.+?)\"", page).group(1)
        key = re.search(r"\"inKey\"\s*:\s*\"(.+?)\"", page).group(1)
        meta_str = get_content(ep.format(vid, key))
        meta_json = json.loads(meta_str)
        if 'errorCode' in meta_json:
            log.wtf(meta_json['errorCode'])
        title = meta_json['meta']['subject']
        videos = meta_json['videos']['list']
        video_list = sorted(videos, key=lambda video: video['encodingOption']['width'])
        video_url = video_list[-1]['source']
        # size = video_list[-1]['size']
        # result wrong size
        size = url_size(video_url)
        print_info(site_info, title, 'mp4', size)
        if not info_only:
            download_urls([video_url], title, 'mp4', size, output_dir, **kwargs)
    except:
        universal_download(url, output_dir, merge=merge, info_only=info_only, **kwargs)

site_info = "naver.com"
download = naver_download_by_url
download_playlist = playlist_not_supported('naver')
