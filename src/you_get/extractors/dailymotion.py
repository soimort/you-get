#!/usr/bin/env python

__all__ = ['dailymotion_download']

from ..common import *

def dailymotion_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    """Downloads Dailymotion videos by URL.
    """

    html = get_content(url)
    info = json.loads(match1(html, r'qualities":({.+?}),"'))
    title = match1(html, r'"video_title"\s*:\s*"(.+?)",')

    for quality in ['720','480','380','240','auto']:
        try:
            real_url = info[quality][0]["url"]
            if real_url:
                break
        except KeyError:
            pass

    type, ext, size = url_info(real_url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Dailymotion.com"
download = dailymotion_download
download_playlist = playlist_not_supported('dailymotion')
