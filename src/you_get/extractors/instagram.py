#!/usr/bin/env python

__all__ = ['instagram_download']

from ..common import *

def instagram_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)

    vid = r1(r'instagram.com/p/([^/]+)/', html)
    description = r1(r'<meta property="og:description" content="([^"]*)"', html)
    title = description + " [" + vid + "]"
    url = r1(r'<meta property="og:video" content="([^"]*)"', html)
    type, ext, size = url_info(url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

site_info = "Instagram.com"
download = instagram_download
download_playlist = playlist_not_supported('instagram')
