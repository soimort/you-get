#!/usr/bin/env python

__all__ = ['tumblr_download']

from ..common import *

import re

def tumblr_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)
    html = parse.unquote(html).replace('\/', '/')
    
    title = unescape_html(r1(r'<meta property="og:title" content="([^"]*)" />', html) or
        r1(r'<meta property="og:description" content="([^"]*)" />', html) or
        r1(r'<title>([^<\n]*)', html)).replace('\n', '')
    real_url = r1(r'source src=\\x22([^\\]+)\\', html)
    if not real_url:
        real_url = r1(r'audio_file=([^&]+)&', html) + '?plead=please-dont-download-this-or-our-lawyers-wont-let-us-host-audio'
    
    type, ext, size = url_info(real_url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Tumblr.com"
download = tumblr_download
download_playlist = playlist_not_supported('tumblr')
