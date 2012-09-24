#!/usr/bin/env python

__all__ = ['dailymotion_download']

from ..common import *

def dailymotion_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)
    html = parse.unquote(html).replace('\/', '/')
    
    title = r1(r'meta property="og:title" content="([^"]+)"', html)
    title = escape_file_path(title)
    
    real_url = r1(r',\"sdURL\"\:\"([^\"]+?)\",', html)
    type, ext, size = url_info(real_url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Dailymotion.com"
download = dailymotion_download
download_playlist = playlist_not_supported('dailymotion')
