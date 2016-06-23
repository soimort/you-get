#!/usr/bin/env python

__all__ = ['facebook_download']

from ..common import *
import json

def facebook_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    html = get_html(url)

    title = r1(r'<title id="pageTitle">(.+)</title>', html)
    sd_urls = [
        unicodize(str.replace(i, '\\/', '/'))
        for i in re.findall(r'"sd_src_no_ratelimit":"([^"]*)"', html)
    ]

    type, ext, size = url_info(sd_urls[0], True)
    size = urls_size(sd_urls)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls(sd_urls, title, ext, size, output_dir, merge=False)

site_info = "Facebook.com"
download = facebook_download
download_playlist = playlist_not_supported('facebook')
