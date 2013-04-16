#!/usr/bin/env python

__all__ = ['googleplus_download']

from ..common import *

import re

def googleplus_download(url, output_dir = '.', merge = True, info_only = False):
    # Percent-encoding Unicode URL
    url = parse.quote(url, safe = ':/+%')
    
    html = get_html(url)
    html = parse.unquote(html).replace('\/', '/')
    
    title = r1(r'<title>(.*)</title>', html) or r1(r'<title>(.*)\n', html) or r1(r'<meta property="og:title" content="([^"]*)"', html)
    
    url2 = r1(r'<a href="([^"]+)" target="_blank" class="Mn" >', html)
    if url2:
        html = get_html(url2)
        html = parse.unquote(html.replace('\/', '/'))
    
    real_url = unicodize(r1(r'"(https://video.googleusercontent.com/[^"]*)",1\]', html).replace('\/', '/'))
    if real_url:
        type, ext, size = url_info(real_url)
    if not real_url or not size:
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
    
    if not ext:
        ext = 'mp4'
    
    response = request.urlopen(request.Request(real_url))
    if response.headers['content-disposition']:
        filename = parse.unquote(r1(r'filename="?(.+)"?', response.headers['content-disposition'])).split('.')
        title = ''.join(filename[:-1])
    
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "plus.google.com"
download = googleplus_download
download_playlist = playlist_not_supported('googleplus')
