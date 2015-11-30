#!/usr/bin/env python

__all__ = ['freesound_download']

from ..common import *

def freesound_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    page = get_html(url)
    
    title = r1(r'<meta property="og:title" content="([^"]*)"', page)
    preview_url = r1(r'<meta property="og:audio" content="([^"]*)"', page)
    
    type, ext, size = url_info(preview_url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([preview_url], title, ext, size, output_dir, merge = merge)

site_info = "Freesound.org"
download = freesound_download
download_playlist = playlist_not_supported('freesound')
