#!/usr/bin/env python

__all__ = ['v1_download']

from ..common import *

def v1_download(url, output_dir = '.', merge = False, info_only = False, **kwargs):
    if (re.match(r'http://www.v1.cn/\d+-\d+-\d+/(\d+).shtml', url) or
    re.match(r'http://v.v1.cn/\d+/\d+/\d+/\d+/(\d+).shtml', url) or 
    re.match(r'http://www.v1.cn/video/v_(\d+).jhtml', url)):
        html = get_content(url)
        match = re.search(r'videoUrl=(.+?)" (.+?)', html)
        if match:
            url = match.group(1)
            title = match1(html, r'<meta name="title" content="([^"]*)"').split('-')[0].strip()
            
            _, ext, size = url_info(url)
            print_info(site_info, title, ext, size)
            if not info_only:
                download_urls([url], title, ext, total_size=None, output_dir=output_dir, merge=merge)

site_info = "V1"
download = v1_download
download_playlist = playlist_not_supported('V1')