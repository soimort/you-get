#!/usr/bin/env python

__all__ = ['googleplus_download']

from ..common import *

def googleplus_download(url, output_dir = '.', merge = True, info_only = False):
    # Percent-encoding Unicode URL
    url = parse.quote(url, safe = ':/')
    
    html = get_html(url)
    html = parse.unquote(html).replace('\/', '/')
    
    title = r1(r'<title>(.*)</title>', html) or r1(r'<title>(.*)\n', html)
    
    url2 = r1(r'"(https\://plus\.google\.com/photos/.*?)",,"image/jpeg","video"\]', html)
    html2 = get_html(url2)
    html2 = parse.unquote(html2.replace('\/', '/'))
    
    real_url = r1(r',\"(http://redirector.googlevideo.com/.*)\"]', html2)
    real_url = unicodize(real_url)
    
    type, ext, size = url_info(real_url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "plus.google.com"
download = googleplus_download
download_playlist = playlist_not_supported('googleplus')
