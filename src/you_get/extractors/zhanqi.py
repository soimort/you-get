#!/usr/bin/env python

__all__ = ['zhanqi_download']

from ..common import *
import re

def zhanqi_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_content(url)
    rtmp_base_patt = r'VideoUrl":"([^"]+)"'
    rtmp_id_patt = r'VideoID":"([^"]+)"'
    title_patt = r'<p class="title-name" title="[^"]+">([^<]+)</p>'
    title_patt_backup = r'<title>([^<]{1,9999})</title>'
    
    rtmp_base = match1(html, rtmp_base_patt).replace('\\/','/')
    rtmp_id = match1(html, rtmp_id_patt).replace('\\/','/')
    title = match1(html, title_patt) or match1(html, title_patt_backup)
    title = unescape_html(title)

    real_url = rtmp_base+'/'+rtmp_id
    
    print_info(site_info, title, 'flv', float('inf'))
    if not info_only:
        download_rtmp_url(real_url, title, 'flv', {}, output_dir, merge = merge)

site_info = "zhanqi.tv"
download = zhanqi_download
download_playlist = playlist_not_supported('zhanqi')
