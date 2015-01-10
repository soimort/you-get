#!/usr/bin/env python

__all__ = ['metacafe_download']

from ..common import *
import urllib.error
from urllib.parse import unquote

def metacafe_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    if re.match(r'http://www.metacafe.com/watch/\w+', url):
        html =get_content(url)
        title = r1(r'<meta property="og:title" content="([^"]*)"', html)
        
        for i in html.split('&'):  #wont bother to use re
            if 'videoURL' in i:
                url_raw = i[9:]
        
        url = unquote(url_raw)
        
        type, ext, size = url_info(url)
        print_info(site_info, title, type, size)
        if not info_only:
            download_urls([url], title, ext, size, output_dir, merge=merge)

site_info = "metacafe"
download = metacafe_download
download_playlist = playlist_not_supported('metacafe')
