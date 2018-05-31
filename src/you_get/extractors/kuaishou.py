#!/usr/bin/env python

import urllib.request
import urllib.parse
import json
import re

from ..util import log
from ..common import get_content, download_urls, print_info, playlist_not_supported, url_size

__all__ = ['kuaishou_download_by_url']


def kuaishou_download_by_url(url, info_only=False, **kwargs):
    page = get_content(url)
    # size = video_list[-1]['size']
    # result wrong size
    try:
        og_video_url = re.search(r"<meta\s+property=\"og:video:url\"\s+content=\"(.+?)\"/>", page).group(1)
        video_url = og_video_url
        title = url.split('/')[-1]
        size = url_size(video_url)
        video_format = video_url.split('.')[-1]
        print_info(site_info, title, video_format, size)
        if not info_only:
            download_urls([video_url], title, video_format, size, **kwargs)
    except:# extract image
        og_image_url = re.search(r"<meta\s+property=\"og:image\"\s+content=\"(.+?)\"/>", page).group(1)
        image_url = og_image_url
        title = url.split('/')[-1]
        size = url_size(image_url)
        image_format = image_url.split('.')[-1]
        print_info(site_info, title, image_format, size)
        if not info_only:
            download_urls([image_url], title, image_format, size, **kwargs)

site_info = "kuaishou.com"
download = kuaishou_download_by_url
download_playlist = playlist_not_supported('kuaishou')
