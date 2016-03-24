#!/usr/bin/env python

__all__ = ['pornhub_download', 'pornhub_download_by_viewkey']

from ..common import *

def pornhub_download_by_viewkey(viewkey, output_dir='.', merge=True, info_only=False):
    """Downloads a Pornhub video by its viewkey"""
    content = get_content('http://www.pornhub.com/embed/{}'.format(viewkey))
    url = match1(content, r'quality_\d+p":"([^"]+)').replace(r"\/", "/")
    if url.startswith('//'): url = 'http:' + url
    title = match1(content, r'<title>([^<]+)')
    _, ext, size = url_info(url)
    
    print_info(site_info, title, ext, size)
    if not info_only:
        download_urls([url], title, ext, size, output_dir=output_dir, merge=merge)

def pornhub_download(url, output_dir='.', merge=True, info_only=False, **kwargs):
    viewkey = match1(url, r'viewkey=([0-9a-z]+)')
    if viewkey is None:
        viewkey = match1(url, r'embed/([0-9a-z]+)')
    if viewkey:
        pornhub_download_by_viewkey(viewkey)

site_info = "Pornhub.com"
download = pornhub_download
download_playlist = playlist_not_supported('Pornhub')