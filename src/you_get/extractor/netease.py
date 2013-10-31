#!/usr/bin/env python

__all__ = ['netease_download']

from ..common import *

def netease_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_decoded_html(url)
    
    title = r1('movieDescription=\'([^\']+)\'', html) or r1('<title>(.+)</title>', html)
    if title[0] == ' ':
        title = title[1:]
    
    src = r1(r'<source src="([^"]+)"', html) or r1(r'<source type="[^"]+" src="([^"]+)"', html)
    
    if src:
        sd_url = r1(r'(.+)-mobile.mp4', src) + ".flv"
        _, _, sd_size = url_info(sd_url)
        
        hd_url = re.sub('/SD/', '/HD/', sd_url)
        _, _, hd_size = url_info(hd_url)
        
        if hd_size > sd_size:
            url, size = hd_url, hd_size
        else:
            url, size = sd_url, sd_size
        ext = 'flv'
        
    else:
        url = r1(r'["\'](.+)-list.m3u8["\']', html) + ".mp4"
        _, _, size = url_info(url)
        ext = 'mp4'
    
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir = output_dir, merge = merge)

site_info = "163.com"
download = netease_download
download_playlist = playlist_not_supported('netease')
