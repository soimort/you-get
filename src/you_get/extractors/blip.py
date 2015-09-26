#!/usr/bin/env python

__all__ = ['blip_download']

from ..common import *

import json

def blip_download(url, output_dir = '.', merge = True, info_only = False, **kwargs):
    p_url = url + "?skin=json&version=2&no_wrap=1"
    html = get_html(p_url)
    metadata = json.loads(html)
    
    title = metadata['Post']['title']
    real_url = metadata['Post']['media']['url']
    type, ext, size = url_info(real_url)
    
    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Blip.tv"
download = blip_download
download_playlist = playlist_not_supported('blip')
