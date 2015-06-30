#!/usr/bin/env python

__all__ = ['tumblr_download']

from ..common import *

import re

def tumblr_download(url, output_dir = '.', merge = True, info_only = False):
    html = parse.unquote(get_html(url)).replace('\/', '/')
    feed = r1(r'<meta property="og:type" content="tumblr-feed:(\w+)" />', html)

    if feed == 'audio':
        real_url = r1(r'source src=\\x22([^\\]+)\\', html)
        if not real_url:
            real_url = r1(r'audio_file=([^&]+)&', html) + '?plead=please-dont-download-this-or-our-lawyers-wont-let-us-host-audio'
    elif feed == 'video':
        iframe_url = r1(r'<iframe src=\'([^\']*)\'', html)
        iframe_html = get_html(iframe_url)
        real_url = r1(r'<source src="([^"]*)"', iframe_html)
    else:
        real_url = r1(r'<source src="([^"]*)"', html)
    
    title = unescape_html(r1(r'<meta property="og:title" content="([^"]*)" />', html) or
        r1(r'<meta property="og:description" content="([^"]*)" />', html) or
        r1(r'<title>([^<\n]*)', html) or url.split("/")[4]).replace('\n', '')
    
    type, ext, size = url_info(real_url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Tumblr.com"
download = tumblr_download
download_playlist = playlist_not_supported('tumblr')
