#!/usr/bin/env python

__all__ = ['jpopsuki_download']

from ..common import *

def jpopsuki_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url, faker=True)
    
    title = r1(r'<meta name="title" content="([^"]*)"', html)
    if title.endswith(' - JPopsuki TV'):
        title = title[:-14]
    
    url = "http://jpopsuki.tv%s" % r1(r'<source src="([^"]*)"', html)
    type, ext, size = url_info(url, faker=True)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge=merge, faker=True)

site_info = "JPopsuki.tv"
download = jpopsuki_download
download_playlist = playlist_not_supported('jpopsuki')
