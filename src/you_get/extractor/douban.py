#!/usr/bin/env python

__all__ = ['douban_download']

from ..common import *

def douban_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)
    
    titles = re.findall(r'"name":"([^"]*)"', html)
    real_urls = [re.sub('\\\\/', '/', i) for i in re.findall(r'"rawUrl":"([^"]*)"', html)]
    
    for i in range(len(titles)):
        title = titles[i]
        real_url = real_urls[i]
        
        type, ext, size = url_info(real_url)
        
        print_info(site_info, title, type, size)
        if not info_only:
            download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Douban.com"
download = douban_download
download_playlist = playlist_not_supported('douban')
