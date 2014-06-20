#!/usr/bin/env python

__all__ = ['vine_download']

from ..common import *

def vine_download(url, output_dir='.', merge=True, info_only=False):
    html = get_html(url)

    vid = r1(r'vine.co/v/([^/]+)/', html)
    title1 = r1(r'<meta property="twitter:title" content="([^"]*)"', html)
    title2 = r1(r'<meta property="twitter:description" content="([^"]*)"', html)
    title = "%s - %s" % (title1, title2) + " [" + vid + "]"
    url = r1(r'<source src="([^"]*)"', html) or r1(r'<meta itemprop="contentURL" content="([^"]*)"', html)
    if url[0:2] == "//":
        url = "http:" + url
    type, ext, size = url_info(url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge = merge)

site_info = "Vine.co"
download = vine_download
download_playlist = playlist_not_supported('vine')
