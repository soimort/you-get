#!/usr/bin/env python

__all__ = ['dailymotion_download']

from ..common import *

def dailymotion_download(url, output_dir = '.', merge = True, info_only = False):
    """Downloads Dailymotion videos by URL.
    """

    id = match1(url, r'/video/([^\?]+)') or match1(url, r'video=([^\?]+)')
    embed_url = 'http://www.dailymotion.com/embed/video/%s' % id
    html = get_content(embed_url)

    info = json.loads(match1(html, r'var\s*info\s*=\s*({.+}),\n'))

    title = info['title']

    for quality in ['stream_h264_hd1080_url', 'stream_h264_hd_url', 'stream_h264_hq_url', 'stream_h264_url', 'stream_h264_ld_url']:
        real_url = info[quality]
        if real_url:
            break

    type, ext, size = url_info(real_url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([real_url], title, ext, size, output_dir, merge = merge)

site_info = "Dailymotion.com"
download = dailymotion_download
download_playlist = playlist_not_supported('dailymotion')
