#!/usr/bin/env python

__all__ = ['googleplus_download']

from ..common import *

import re

def googleplus_download(url, output_dir = '.', merge = True, info_only = False):
    # Percent-encoding Unicode URL
    url = parse.quote(url, safe = ':/+%')
    
    html = get_html(url)
    html = parse.unquote(html).replace('\/', '/')
    
    title = r1(r'<title>(.*)</title>', html) or r1(r'<title>(.*)\n', html)
    
    url2 = r1(r'"(https\://plus\.google\.com/photos/.*?)",,"image/jpeg","video"\]', html)
    if url2:
        html = get_html(url2)
        html = parse.unquote(html.replace('\/', '/'))
    
    url_data = re.findall(r'(\[[^\[\"]+\"http://redirector.googlevideo.com/.*\"\])', html)
    
    for itag in [
        '38',
        '46', '37',
        '102', '45', '22',
        '84',
        '120',
        '85',
        '44', '35',
        '101', '100', '43', '34', '82', '18',
        '6',
        '83', '5', '36',
        '17',
        '13',
    ]:
        real_url = None
        for url_item in url_data:
            if itag == str(eval(url_item)[0]):
                real_url = eval(url_item)[3]
                break
        if real_url:
            break
    real_url = unicodize(real_url)
    
    type, ext, size = url_info(real_url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "plus.google.com"
download = googleplus_download
download_playlist = playlist_not_supported('googleplus')
