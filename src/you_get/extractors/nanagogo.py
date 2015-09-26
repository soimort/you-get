#!/usr/bin/env python

__all__ = ['nanagogo_download']

from ..common import *

def nanagogo_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)
    title = r1(r'<meta property="og:title" content="([^"]*)"', html)
    postId = r1(r'postId\s*:\s*"([^"]*)"', html)
    title += ' - ' + postId
    source = r1(r'<meta property="og:video" content="([^"]*)"', html)
    mime, ext, size = url_info(source)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([source], title, ext, size, output_dir, merge=merge)

site_info = "7gogo.jp"
download = nanagogo_download
download_playlist = playlist_not_supported('nanagogo')
