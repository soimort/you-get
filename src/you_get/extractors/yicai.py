#!/usr/bin/env python

__all__ = ['yicai_download']

from ..common import *

def yicai_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if "www.yicai.com" in url:
        url = url.replace('www.yicai.com','m.yicai.com')
        html = get_content(url)
        title = match1(html, r'<h1 class="f-ff3">(.+)</h1>')
        url = match1(html, r'<source.+?src="([^"]+)"')
        _, ext, size = url_info(url)
        print_info(site_info, title, ext, size)
        if not info_only:
            download_urls([url], title, ext, size, output_dir = output_dir, merge = merge)

site_info = "*.yicai.com/video"
download = yicai_download
download_playlist = playlist_not_supported('yicai')
