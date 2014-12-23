#!/usr/bin/env python3

__all__ = ['redtube_download']
from ..common import *

def redtube_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_content(url)

    video_url = match1(html, r'<source src="([^"]+)"')
    title = match1(html,r'<title>(.*?)</title>').rsplit('|', maxsplit=1)[0].strip()
    (type, ext, size) = url_info(video_url)
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([video_url], title, ext, size, output_dir, merge = merge)

site_info = "redtube.com"
download= redtube_download
download_playlist = playlist_not_supported('redtube')
