#!/usr/bin/env python

__all__ = ['vk_download']

from ..common import *

def vk_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    video_page = get_content(url)
    title = unescape_html(r1(r'"title":"([^"]+)"', video_page))
    info = dict(re.findall(r'\\"url(\d+)\\":\\"([^"]+)\\"', video_page))
    for quality in ['1080', '720', '480', '360', '240']:
        if quality in info:
            url = re.sub(r'\\\\\\/', r'/', info[quality])
            break
    assert url

    type, ext, size = url_info(url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge=merge)

site_info = "VK.com"
download = vk_download
download_playlist = playlist_not_supported('vk')
