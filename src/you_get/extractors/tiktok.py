#!/usr/bin/env python

__all__ = ['tiktok_download']

from ..common import *

def tiktok_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url, faker=True)
    title = r1(r'<title.*?>(.*?)</title>', html)
    video_id = r1(r'/video/(\d+)', url) or r1(r'musical\?id=(\d+)', html)
    title = '%s [%s]' % (title, video_id)
    source = r1(r'<video .*?src="([^"]+)"', html)
    mime, ext, size = url_info(source)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([source], title, ext, size, output_dir, merge=merge)

site_info = "TikTok.com"
download = tiktok_download
download_playlist = playlist_not_supported('tiktok')
