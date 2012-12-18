#!/usr/bin/env python

__all__ = ['tumblr_download']

from ..common import *

import re

def tumblr_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)
    html = parse.unquote(html).replace('\/', '/')
    
    title = r1(r'<title>(.*)</title>', html) or r1(r'<title>(.*)\n', html)
    real_url = r1(r'source src=\\x22([^\\]+)\\', html)
    
    type, ext, size = url_info(real_url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Tumblr.com"
download = tumblr_download
download_playlist = playlist_not_supported('tumblr')
