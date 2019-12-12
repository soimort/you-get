#!/usr/bin/env python

__all__ = ['facebook_download']

from ..common import *
import json

def facebook_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    url = re.sub(r'//.*?facebook.com','//facebook.com',url)
    html = get_html(url)

    title = r1(r'<title id="pageTitle">(.+)</title>', html)

    if title is None:
      title = url

    sd_urls = list(set([
        unicodize(str.replace(i, '\\/', '/'))
        for i in re.findall(r'sd_src_no_ratelimit:"([^"]*)"', html)
    ]))
    hd_urls = list(set([
        unicodize(str.replace(i, '\\/', '/'))
        for i in re.findall(r'hd_src_no_ratelimit:"([^"]*)"', html)
    ]))
    urls = hd_urls if hd_urls else sd_urls

    type, ext, size = url_info(urls[0], True)
    size = urls_size(urls)

    print_info(site_info, title, type, size)
    if not info_only:
        download_urls(urls, title, ext, size, output_dir, merge=False)

site_info = "Facebook.com"
download = facebook_download
download_playlist = playlist_not_supported('facebook')
