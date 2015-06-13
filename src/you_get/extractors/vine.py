#!/usr/bin/env python

__all__ = ['vine_download']

from ..common import *

def vine_download(url, output_dir='.', merge=True, info_only=False):
    html = get_html(url)

    vid = r1(r'vine.co/v/([^/]+)', url)
    title1 = r1(r'<meta property="twitter:title" content="([^"]*)"', html)
    title2 = r1(r'<meta property="twitter:description" content="([^"]*)"', html)
    title = "{} - {} [{}]".format(title1, title2, vid)
    stream = r1(r'<meta property="twitter:player:stream" content="([^"]*)">', html)
    mime, ext, size = url_info(stream)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([stream], title, ext, size, output_dir, merge=merge)

site_info = "Vine.co"
download = vine_download
download_playlist = playlist_not_supported('vine')
