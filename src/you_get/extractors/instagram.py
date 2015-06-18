#!/usr/bin/env python

__all__ = ['instagram_download']

from ..common import *

def instagram_download(url, output_dir = '.', merge = True, info_only = False):
    html = get_html(url)

    vid = r1(r'instagram.com/p/([^/]+)', url)
    description = r1(r'<meta property="og:title" content="([^"]*)"', html)
    title = "{} [{}]".format(description.replace("\n", " "), vid)
    stream = r1(r'<meta property="og:video" content="([^"]*)"', html)
    mime, ext, size = url_info(stream)

    print_info(site_info, title, mime, size)
    if not info_only:
        download_urls([stream], title, ext, size, output_dir, merge=merge)

site_info = "Instagram.com"
download = instagram_download
download_playlist = playlist_not_supported('instagram')
