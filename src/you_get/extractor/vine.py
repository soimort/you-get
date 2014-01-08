#!/usr/bin/env python

__all__ = ['vine_download']

from ..common import *

def vine_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)
    
    title = r1(r'<meta property="og:title" content="([^"]*)"', html)
    url = r1(r'<source src="([^"]*)"', html)
    if url[0:2] == "//":
        url = "http:" + url
    type, ext, size = url_info(url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

site_info = "Vine.co"
download = vine_download
download_playlist = playlist_not_supported('vine')
