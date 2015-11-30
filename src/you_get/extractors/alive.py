#!/usr/bin/env python

__all__ = ['alive_download']

from ..common import *

def alive_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    html = get_html(url)
    
    title = r1(r'<meta property="og:title" content="([^"]+)"', html)
    
    url = r1(r'file: "(http://alive[^"]+)"', html)
    type, ext, size = url_info(url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

site_info = "Alive.in.th"
download = alive_download
download_playlist = playlist_not_supported('alive')
