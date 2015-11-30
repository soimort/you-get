#!/usr/bin/env python

__all__ = ['magisto_download']

from ..common import *

def magisto_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)

    title1 = r1(r'<meta name="twitter:title" content="([^"]*)"', html)
    title2 = r1(r'<meta name="twitter:description" content="([^"]*)"', html)
    video_hash = r1(r'http://www.magisto.com/video/([^/]+)', url)
    title = "%s %s - %s" % (title1, title2, video_hash)
    url = r1(r'<source type="[^"]+" src="([^"]*)"', html)
    type, ext, size = url_info(url)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir, merge=merge)

site_info = "Magisto.com"
download = magisto_download
download_playlist = playlist_not_supported('magisto')
