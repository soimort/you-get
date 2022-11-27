#!/usr/bin/env python

import json
import re
import urllib.parse
import urllib.request

from ..common import (download_urls, get_content, playlist_not_supported,
                      print_info, url_size)
from ..util import log

__all__ = ['kuaishou_download_by_url']


def kuaishou_download_by_url(url, info_only=False, **kwargs):
    page = get_content(url)
    # size = video_list[-1]['size']
    # result wrong size
    try:
        search_result=re.search(r"\"playUrls\":\[(\{\"quality\"\:\"\w+\",\"url\":\".*?\"\})+\]", page)
        all_video_info_str = search_result.group(1)
        all_video_infos=re.findall(r"\{\"quality\"\:\"(\w+)\",\"url\":\"(.*?)\"\}", all_video_info_str)
        # get the one of the best quality
        video_url = all_video_infos[0][1].encode("utf-8").decode('unicode-escape')
        title = re.search(r"<meta charset=UTF-8><title>(.*?)</title>", page).group(1)
        size = url_size(video_url)
        video_format = "flv"#video_url.split('.')[-1]
        print_info(site_info, title, video_format, size)
        if not info_only:
            download_urls([video_url], title, video_format, size, **kwargs)
    except Exception:# extract image
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
