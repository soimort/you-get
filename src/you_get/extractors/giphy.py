#!/usr/bin/env python

__all__ = ['giphy_download']

from ..common import *
import json

def giphy_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)

    url = list(set([
        unicodize(str.replace(i, '\\/', '/'))
        for i in re.findall(r'<meta property="og:video:secure_url" content="(.*?)">', html)
    ]))

    title = r1(r'<meta property="og:title" content="(.*?)">', html)

    if title is None:
      title = url[0]

    type, ext, size = url_info(url[0], True)
    size = urls_size(url)

    type = "video/mp4"
    ext = "mp4"

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls(url, title, ext, size, output_dir, merge=False)

site_info = "Giphy.com"
download = giphy_download
download_playlist = playlist_not_supported('giphy')
