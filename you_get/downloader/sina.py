#!/usr/bin/env python

__all__ = ['sina_download', 'sina_download_by_id']

from ..common import *

import re

def video_info(id):
    xml = get_decoded_html('http://v.iask.com/v_play.php?vid=%s' % id)
    urls = re.findall(r'<url>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</url>', xml)
    name = r1(r'<vname>(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?</vname>', xml)
    vstr = r1(r'<vstr>(?:<!\[CDATA\[)?(.+?)(?:\]\]>)?</vstr>', xml)
    return urls, name, vstr

def sina_download_by_id(id, title = None, output_dir = '.', merge = True, info_only = False):
    urls, name, vstr = video_info(id)
    title = title or name
    assert title
    size = 0
    for url in urls:
        _, _, temp = url_info(url)
        size += temp
    
    print_info(site_info, title, 'flv', size)
    if not info_only:
        download_urls(urls, title, 'flv', size, output_dir = output_dir, merge = merge)

def sina_download(url, output_dir = '.', merge = True, info_only = False):
    id = r1(r'ipad_vid:\'(\d+)\',', get_html(url))
    sina_download_by_id(id, output_dir = output_dir, merge = merge, info_only = info_only)

site_info = "Sina.com"
download = sina_download
download_playlist = playlist_not_supported('sina')
